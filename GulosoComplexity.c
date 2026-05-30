#include <ctype.h>
#include <errno.h>
#include <float.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MT_N 624
#define MT_M 397
#define MT_MATRIX_A 0x9908b0dfUL
#define MT_UPPER_MASK 0x80000000UL
#define MT_LOWER_MASK 0x7fffffffUL
#define MAX_SEEDS 64

typedef struct {
    uint32_t mt[MT_N];
    int index;
} PythonRandom;

typedef struct {
    int from;
    int to;
} Path;

typedef struct {
    char **items;
    int count;
    int capacity;
} StringMap;

typedef struct {
    char *header_line;
    char **headers;
    char **row_lines;
    char ***fields;
    int rows;
    int columns;
    int row_capacity;
} RawCsv;

typedef struct {
    double *x;
    int *y;
    int rows;
    int features;
    int classes;
    int target_col;
} Dataset;

typedef struct {
    const char *input_path;
    const char *output_path;
    const char *target_arg;
    double initial_pheromone;
    double evaporation_rate;
    double q;
    uint32_t seeds[MAX_SEEDS];
    int seed_count;
} Config;

static void *xmalloc(size_t size) {
    void *ptr = malloc(size);
    if (!ptr) {
        fprintf(stderr, "Erro: memoria insuficiente ao alocar %zu bytes.\n", size);
        exit(EXIT_FAILURE);
    }
    return ptr;
}

static void *xcalloc(size_t count, size_t size) {
    void *ptr = calloc(count, size);
    if (!ptr) {
        fprintf(stderr, "Erro: memoria insuficiente ao alocar %zu bytes.\n", count * size);
        exit(EXIT_FAILURE);
    }
    return ptr;
}

static void *xrealloc(void *old, size_t size) {
    void *ptr = realloc(old, size);
    if (!ptr) {
        fprintf(stderr, "Erro: memoria insuficiente ao realocar %zu bytes.\n", size);
        exit(EXIT_FAILURE);
    }
    return ptr;
}

static char *xstrdup(const char *text) {
    size_t len = strlen(text);
    char *copy = (char *)xmalloc(len + 1);
    memcpy(copy, text, len + 1);
    return copy;
}

static double elapsed_seconds(clock_t start, clock_t end) {
    return (double)(end - start) / (double)CLOCKS_PER_SEC;
}

static double mean_double(const double *values, int count) {
    double sum = 0.0;
    int i;
    for (i = 0; i < count; i++) {
        sum += values[i];
    }
    return count > 0 ? sum / (double)count : 0.0;
}

static double stdev_double(const double *values, int count) {
    double mean;
    double sum = 0.0;
    int i;

    if (count <= 1) {
        return 0.0;
    }

    mean = mean_double(values, count);
    for (i = 0; i < count; i++) {
        double diff = values[i] - mean;
        sum += diff * diff;
    }
    return sqrt(sum / (double)(count - 1));
}

static double mean_int(const int *values, int count) {
    double sum = 0.0;
    int i;
    for (i = 0; i < count; i++) {
        sum += (double)values[i];
    }
    return count > 0 ? sum / (double)count : 0.0;
}

static void py_init_genrand(PythonRandom *rng, uint32_t seed) {
    rng->mt[0] = seed;
    for (rng->index = 1; rng->index < MT_N; rng->index++) {
        rng->mt[rng->index] =
            (uint32_t)(1812433253UL * (rng->mt[rng->index - 1] ^
            (rng->mt[rng->index - 1] >> 30)) + (uint32_t)rng->index);
    }
}

static void py_init_by_array(PythonRandom *rng, const uint32_t init_key[], int key_length) {
    int i = 1;
    int j = 0;
    int k = MT_N > key_length ? MT_N : key_length;
    py_init_genrand(rng, 19650218UL);
    for (; k; k--) {
        rng->mt[i] = (uint32_t)((rng->mt[i] ^
            ((rng->mt[i - 1] ^ (rng->mt[i - 1] >> 30)) * 1664525UL)) +
            init_key[j] + (uint32_t)j);
        i++;
        j++;
        if (i >= MT_N) {
            rng->mt[0] = rng->mt[MT_N - 1];
            i = 1;
        }
        if (j >= key_length) {
            j = 0;
        }
    }
    for (k = MT_N - 1; k; k--) {
        rng->mt[i] = (uint32_t)((rng->mt[i] ^
            ((rng->mt[i - 1] ^ (rng->mt[i - 1] >> 30)) * 1566083941UL)) -
            (uint32_t)i);
        i++;
        if (i >= MT_N) {
            rng->mt[0] = rng->mt[MT_N - 1];
            i = 1;
        }
    }
    rng->mt[0] = 0x80000000UL;
    rng->index = MT_N;
}

static void py_random_seed(PythonRandom *rng, uint32_t seed) {
    uint32_t key[1];
    key[0] = seed;
    py_init_by_array(rng, key, 1);
}

static uint32_t py_genrand_uint32(PythonRandom *rng) {
    uint32_t y;
    static const uint32_t mag01[2] = {0x0UL, MT_MATRIX_A};

    if (rng->index >= MT_N) {
        int kk;
        for (kk = 0; kk < MT_N - MT_M; kk++) {
            y = (rng->mt[kk] & MT_UPPER_MASK) | (rng->mt[kk + 1] & MT_LOWER_MASK);
            rng->mt[kk] = rng->mt[kk + MT_M] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        for (; kk < MT_N - 1; kk++) {
            y = (rng->mt[kk] & MT_UPPER_MASK) | (rng->mt[kk + 1] & MT_LOWER_MASK);
            rng->mt[kk] = rng->mt[kk + (MT_M - MT_N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        y = (rng->mt[MT_N - 1] & MT_UPPER_MASK) | (rng->mt[0] & MT_LOWER_MASK);
        rng->mt[MT_N - 1] = rng->mt[MT_M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];
        rng->index = 0;
    }

    y = rng->mt[rng->index++];
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680UL;
    y ^= (y << 15) & 0xefc60000UL;
    y ^= (y >> 18);
    return y;
}

static int py_randint_0_1(PythonRandom *rng) {
    uint32_t value;
    do {
        value = py_genrand_uint32(rng) >> 30;
    } while (value >= 2);
    return (int)value;
}

static char *read_line(FILE *file) {
    size_t capacity = 256;
    size_t length = 0;
    int ch;
    char *line = (char *)xmalloc(capacity);

    while ((ch = fgetc(file)) != EOF) {
        if (ch == '\n') {
            break;
        }
        if (length + 1 >= capacity) {
            capacity *= 2;
            line = (char *)xrealloc(line, capacity);
        }
        line[length++] = (char)ch;
    }

    if (ch == EOF && length == 0) {
        free(line);
        return NULL;
    }

    while (length > 0 && line[length - 1] == '\r') {
        length--;
    }
    line[length] = '\0';
    return line;
}

static char *copy_trimmed(const char *start, size_t length) {
    while (length > 0 && isspace((unsigned char)*start)) {
        start++;
        length--;
    }
    while (length > 0 && isspace((unsigned char)start[length - 1])) {
        length--;
    }

    char *copy = (char *)xmalloc(length + 1);
    memcpy(copy, start, length);
    copy[length] = '\0';
    return copy;
}

static char **split_csv_simple(const char *line, int *count_out) {
    int count = 1;
    const char *p;
    const char *start;
    char **fields;
    int index = 0;

    for (p = line; *p; p++) {
        if (*p == ',') {
            count++;
        }
    }

    fields = (char **)xmalloc(sizeof(char *) * (size_t)count);
    start = line;
    for (p = line; ; p++) {
        if (*p == ',' || *p == '\0') {
            fields[index++] = copy_trimmed(start, (size_t)(p - start));
            if (*p == '\0') {
                break;
            }
            start = p + 1;
        }
    }

    *count_out = count;
    return fields;
}

static void free_fields(char **fields, int count) {
    int i;
    if (!fields) {
        return;
    }
    for (i = 0; i < count; i++) {
        free(fields[i]);
    }
    free(fields);
}

static RawCsv read_csv(const char *path) {
    FILE *file = fopen(path, "rb");
    RawCsv csv;
    char *line;
    int column_count;

    memset(&csv, 0, sizeof(csv));
    if (!file) {
        fprintf(stderr, "Erro: nao foi possivel abrir '%s'.\n", path);
        exit(EXIT_FAILURE);
    }

    csv.header_line = read_line(file);
    if (!csv.header_line) {
        fprintf(stderr, "Erro: CSV vazio em '%s'.\n", path);
        fclose(file);
        exit(EXIT_FAILURE);
    }

    csv.headers = split_csv_simple(csv.header_line, &csv.columns);
    csv.row_capacity = 256;
    csv.row_lines = (char **)xmalloc(sizeof(char *) * (size_t)csv.row_capacity);
    csv.fields = (char ***)xmalloc(sizeof(char **) * (size_t)csv.row_capacity);

    while ((line = read_line(file)) != NULL) {
        if (line[0] == '\0') {
            free(line);
            continue;
        }
        if (csv.rows >= csv.row_capacity) {
            csv.row_capacity *= 2;
            csv.row_lines = (char **)xrealloc(csv.row_lines,
                sizeof(char *) * (size_t)csv.row_capacity);
            csv.fields = (char ***)xrealloc(csv.fields,
                sizeof(char **) * (size_t)csv.row_capacity);
        }

        csv.fields[csv.rows] = split_csv_simple(line, &column_count);
        if (column_count != csv.columns) {
            fprintf(stderr,
                "Erro: linha %d possui %d colunas, mas o cabecalho possui %d.\n",
                csv.rows + 2, column_count, csv.columns);
            fclose(file);
            exit(EXIT_FAILURE);
        }
        csv.row_lines[csv.rows] = line;
        csv.rows++;
    }

    fclose(file);
    return csv;
}

static void free_csv(RawCsv *csv) {
    int i;
    if (!csv) {
        return;
    }
    free(csv->header_line);
    free_fields(csv->headers, csv->columns);
    for (i = 0; i < csv->rows; i++) {
        free(csv->row_lines[i]);
        free_fields(csv->fields[i], csv->columns);
    }
    free(csv->row_lines);
    free(csv->fields);
}

static void string_map_add_capacity(StringMap *map) {
    if (map->count >= map->capacity) {
        map->capacity = map->capacity == 0 ? 8 : map->capacity * 2;
        map->items = (char **)xrealloc(map->items, sizeof(char *) * (size_t)map->capacity);
    }
}

static int string_map_get_or_add(StringMap *map, const char *value) {
    int i;
    for (i = 0; i < map->count; i++) {
        if (strcmp(map->items[i], value) == 0) {
            return i;
        }
    }
    string_map_add_capacity(map);
    map->items[map->count] = xstrdup(value);
    return map->count++;
}

static void free_string_map(StringMap *map) {
    int i;
    for (i = 0; i < map->count; i++) {
        free(map->items[i]);
    }
    free(map->items);
}

static int parse_double_strict(const char *text, double *value_out) {
    char *end;
    errno = 0;
    if (text[0] == '\0') {
        return 0;
    }
    *value_out = strtod(text, &end);
    if (text == end || errno == ERANGE) {
        return 0;
    }
    while (*end) {
        if (!isspace((unsigned char)*end)) {
            return 0;
        }
        end++;
    }
    return 1;
}

static uint32_t parse_seed_strict(const char *text) {
    char *end;
    unsigned long value;

    errno = 0;
    value = strtoul(text, &end, 10);
    if (errno != 0 || *end != '\0') {
        fprintf(stderr, "Erro: seed invalida '%s'.\n", text);
        exit(EXIT_FAILURE);
    }
    return (uint32_t)value;
}

static void parse_seed_list(const char *text, Config *config) {
    char *copy = xstrdup(text);
    char *token = strtok(copy, ",");

    config->seed_count = 0;
    while (token != NULL) {
        while (*token && isspace((unsigned char)*token)) {
            token++;
        }
        if (*token != '\0') {
            char *end = token + strlen(token);
            while (end > token && isspace((unsigned char)end[-1])) {
                end--;
            }
            *end = '\0';

            if (config->seed_count >= MAX_SEEDS) {
                fprintf(stderr, "Erro: no maximo %d seeds sao suportadas.\n", MAX_SEEDS);
                free(copy);
                exit(EXIT_FAILURE);
            }
            config->seeds[config->seed_count++] = parse_seed_strict(token);
        }
        token = strtok(NULL, ",");
    }

    free(copy);
    if (config->seed_count == 0) {
        fprintf(stderr, "Erro: informe pelo menos uma seed.\n");
        exit(EXIT_FAILURE);
    }
}

static int resolve_target_column(const RawCsv *csv, const char *target_arg) {
    int i;
    char *end;
    long numeric;

    if (!target_arg) {
        return csv->columns - 1;
    }

    for (i = 0; i < csv->columns; i++) {
        if (strcmp(csv->headers[i], target_arg) == 0) {
            return i;
        }
    }

    errno = 0;
    numeric = strtol(target_arg, &end, 10);
    if (errno == 0 && *end == '\0') {
        if (numeric >= 1 && numeric <= csv->columns) {
            return (int)numeric - 1;
        }
        if (numeric >= 0 && numeric < csv->columns) {
            return (int)numeric;
        }
    }

    fprintf(stderr, "Erro: coluna alvo '%s' nao encontrada.\n", target_arg);
    exit(EXIT_FAILURE);
}

static Dataset build_dataset(const RawCsv *csv, int target_col) {
    Dataset dataset;
    int *is_numeric = (int *)xmalloc(sizeof(int) * (size_t)csv->columns);
    StringMap *feature_maps = (StringMap *)xcalloc((size_t)csv->columns, sizeof(StringMap));
    StringMap label_map;
    int r;
    int c;
    int feature_index;
    double value;

    memset(&dataset, 0, sizeof(dataset));
    memset(&label_map, 0, sizeof(label_map));

    dataset.rows = csv->rows;
    dataset.features = csv->columns - 1;
    dataset.target_col = target_col;
    dataset.x = (double *)xmalloc(sizeof(double) * (size_t)dataset.rows * (size_t)dataset.features);
    dataset.y = (int *)xmalloc(sizeof(int) * (size_t)dataset.rows);

    for (c = 0; c < csv->columns; c++) {
        is_numeric[c] = 1;
    }

    for (r = 0; r < csv->rows; r++) {
        for (c = 0; c < csv->columns; c++) {
            if (c == target_col) {
                continue;
            }
            if (!parse_double_strict(csv->fields[r][c], &value)) {
                is_numeric[c] = 0;
            }
        }
    }

    for (r = 0; r < csv->rows; r++) {
        feature_index = 0;
        for (c = 0; c < csv->columns; c++) {
            if (c == target_col) {
                continue;
            }
            if (is_numeric[c]) {
                parse_double_strict(csv->fields[r][c], &value);
                dataset.x[(size_t)r * (size_t)dataset.features + (size_t)feature_index] = value;
            } else {
                int encoded = string_map_get_or_add(&feature_maps[c], csv->fields[r][c]);
                dataset.x[(size_t)r * (size_t)dataset.features + (size_t)feature_index] =
                    (double)encoded;
            }
            feature_index++;
        }
        dataset.y[r] = string_map_get_or_add(&label_map, csv->fields[r][target_col]);
    }

    dataset.classes = label_map.count;

    for (c = 0; c < csv->columns; c++) {
        free_string_map(&feature_maps[c]);
    }
    free(feature_maps);
    free_string_map(&label_map);
    free(is_numeric);
    return dataset;
}

static void free_dataset(Dataset *dataset) {
    free(dataset->x);
    free(dataset->y);
}

static double *calculate_pairwise_distances(const Dataset *dataset) {
    int n = dataset->rows;
    int features = dataset->features;
    double *distances = (double *)xcalloc((size_t)n * (size_t)n, sizeof(double));
    double *norms = (double *)xcalloc((size_t)n, sizeof(double));
    int i;
    int j;
    int k;

    for (i = 0; i < n; i++) {
        double norm = 0.0;
        for (k = 0; k < features; k++) {
            double value = dataset->x[(size_t)i * (size_t)features + (size_t)k];
            norm += value * value;
        }
        norms[i] = norm;
    }

    for (i = 0; i < n; i++) {
        distances[(size_t)i * (size_t)n + (size_t)i] = 0.0;
        for (j = i + 1; j < n; j++) {
            double dot = 0.0;
            double squared_distance;
            for (k = 0; k < features; k++) {
                dot += dataset->x[(size_t)i * (size_t)features + (size_t)k] *
                    dataset->x[(size_t)j * (size_t)features + (size_t)k];
            }
            squared_distance = norms[i] + norms[j] - 2.0 * dot;
            if (squared_distance < 0.0) {
                squared_distance = 0.0;
            }
            distances[(size_t)i * (size_t)n + (size_t)j] = sqrt(squared_distance);
            distances[(size_t)j * (size_t)n + (size_t)i] =
                distances[(size_t)i * (size_t)n + (size_t)j];
        }
    }
    free(norms);
    return distances;
}

static double *create_pheromone_trails(int n, double initial_pheromone) {
    double *trails = (double *)xmalloc(sizeof(double) * (size_t)n * (size_t)n);
    int i;
    int j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            trails[(size_t)i * (size_t)n + (size_t)j] = (i == j) ? 0.0 : initial_pheromone;
        }
    }
    return trails;
}

static signed char *create_colony(int n, long long *remaining_unknown) {
    signed char *colony = (signed char *)xmalloc((size_t)n * (size_t)n);
    int i;
    memset(colony, -1, (size_t)n * (size_t)n);
    for (i = 0; i < n; i++) {
        colony[(size_t)i * (size_t)n + (size_t)i] = 1;
    }
    *remaining_unknown = (long long)n * (long long)n - (long long)n;
    return colony;
}

static void initialize_ant_choices(Path *paths, int *path_lengths, int n) {
    int i;
    for (i = 0; i < n; i++) {
        paths[(size_t)i * (size_t)n].from = i;
        paths[(size_t)i * (size_t)n].to = i;
        path_lengths[i] = 1;
    }
}

static int find_best_available(const signed char *ant, const double *pheromone_row, int n) {
    int best = -1;
    double best_value = -DBL_MAX;
    int j;

    for (j = 0; j < n; j++) {
        if (ant[j] < 0) {
            double value = pheromone_row[j];
            if (best < 0 || value > best_value ||
                (value == best_value && j > best)) {
                best = j;
                best_value = value;
            }
        }
    }
    return best;
}

static void choose_paths_greedy(signed char *colony, Path *paths, int *path_lengths,
    const double *pheromone, int n, long long *remaining_unknown, PythonRandom *rng) {
    int ant_index;

    for (ant_index = 0; ant_index < n; ant_index++) {
        signed char *ant = &colony[(size_t)ant_index * (size_t)n];
        if (path_lengths[ant_index] >= n) {
            continue;
        }

        for (;;) {
            Path last = paths[(size_t)ant_index * (size_t)n +
                (size_t)path_lengths[ant_index] - 1U];
            const double *pheromone_row = &pheromone[(size_t)last.to * (size_t)n];
            int next_instance = find_best_available(ant, pheromone_row, n);

            if (next_instance < 0) {
                break;
            }

            if (py_randint_0_1(rng) != 0) {
                size_t path_pos = (size_t)ant_index * (size_t)n +
                    (size_t)path_lengths[ant_index];
                paths[path_pos].from = last.to;
                paths[path_pos].to = next_instance;
                path_lengths[ant_index]++;
                ant[next_instance] = 1;
                (*remaining_unknown)--;
                break;
            }

            ant[next_instance] = 0;
            (*remaining_unknown)--;
        }
    }
}

static double pheromone_deposit_for_ant(const Path *paths, int length,
    const double *distances, int n, double q) {
    double tour_length = 0.0;
    int i;

    for (i = 0; i < length; i++) {
        int from = paths[i].from;
        int to = paths[i].to;
        tour_length += distances[(size_t)from * (size_t)n + (size_t)to];
    }

    if (tour_length == 0.0) {
        return 0.0;
    }
    return q / tour_length;
}

static void update_pheromones(double *pheromone, const Path *paths, const int *path_lengths,
    const double *distances, int n, double q, double evaporation_rate) {
    int ant_index;
    size_t total = (size_t)n * (size_t)n;
    size_t idx;
    double evaporation_factor = 1.0 - evaporation_rate;

    for (ant_index = 0; ant_index < n; ant_index++) {
        const Path *ant_paths = &paths[(size_t)ant_index * (size_t)n];
        double deposit = pheromone_deposit_for_ant(ant_paths, path_lengths[ant_index],
            distances, n, q);
        int p;
        for (p = 1; p < path_lengths[ant_index]; p++) {
            int from = ant_paths[p].from;
            int to = ant_paths[p].to;
            pheromone[(size_t)from * (size_t)n + (size_t)to] += deposit;
        }
    }

    for (idx = 0; idx < total; idx++) {
        pheromone[idx] *= evaporation_factor;
    }
}

static int *get_best_solution(const signed char *colony, const int *labels,
    const double *distances, int n, int *selected_count_out, double *accuracy_out) {
    int best_ant = 0;
    int best_correct = -1;
    int ant_index;
    int *selected_indices;
    int selected_count = 0;
    int j;

    for (ant_index = 0; ant_index < n; ant_index++) {
        const signed char *solution = &colony[(size_t)ant_index * (size_t)n];
        int correct = 0;
        int row;

        for (row = 0; row < n; row++) {
            double best_distance = DBL_MAX;
            int predicted = -1;

            for (j = 0; j < n; j++) {
                if (solution[j] != 0) {
                    double distance = distances[(size_t)row * (size_t)n + (size_t)j];
                    if (distance < best_distance) {
                        best_distance = distance;
                        predicted = labels[j];
                    }
                }
            }

            if (predicted == labels[row]) {
                correct++;
            }
        }

        if (correct > best_correct) {
            best_correct = correct;
            best_ant = ant_index;
        }
    }

    for (j = 0; j < n; j++) {
        if (colony[(size_t)best_ant * (size_t)n + (size_t)j] != 0) {
            selected_count++;
        }
    }

    selected_indices = (int *)xmalloc(sizeof(int) * (size_t)selected_count);
    selected_count = 0;
    for (j = 0; j < n; j++) {
        if (colony[(size_t)best_ant * (size_t)n + (size_t)j] != 0) {
            selected_indices[selected_count++] = j;
        }
    }

    *selected_count_out = selected_count;
    *accuracy_out = (double)best_correct / (double)n;
    return selected_indices;
}

static int *run_colony(const Dataset *dataset, double initial_pheromone,
    double evaporation_rate, double q, uint32_t seed, int *selected_count_out,
    double *best_accuracy_out, double *aco_time_out, double *knn_time_out) {
    int n = dataset->rows;
    double *distances;
    double *pheromone;
    signed char *colony;
    Path *paths;
    int *path_lengths;
    long long remaining_unknown;
    int iteration = 0;
    PythonRandom rng;
    int *selected_indices;
    clock_t aco_start;
    clock_t aco_end;
    clock_t knn_start;
    clock_t knn_end;

    distances = calculate_pairwise_distances(dataset);
    pheromone = create_pheromone_trails(n, initial_pheromone);
    colony = create_colony(n, &remaining_unknown);
    paths = (Path *)xmalloc(sizeof(Path) * (size_t)n * (size_t)n);
    path_lengths = (int *)xmalloc(sizeof(int) * (size_t)n);
    initialize_ant_choices(paths, path_lengths, n);
    py_random_seed(&rng, seed);

    aco_start = clock();
    while (remaining_unknown > 0) {
        iteration++;
        choose_paths_greedy(colony, paths, path_lengths, pheromone, n,
            &remaining_unknown, &rng);
        update_pheromones(pheromone, paths, path_lengths, distances, n, q,
            evaporation_rate);
        if (iteration % 100 == 0 || remaining_unknown == 0) {
            printf("Iteracao %d concluida; posicoes indefinidas restantes: %lld\n",
                iteration, remaining_unknown);
        }
    }
    aco_end = clock();

    knn_start = clock();
    selected_indices = get_best_solution(colony, dataset->y, distances, n,
        selected_count_out, best_accuracy_out);
    knn_end = clock();

    *aco_time_out = elapsed_seconds(aco_start, aco_end);
    *knn_time_out = elapsed_seconds(knn_start, knn_end);

    free(distances);
    free(pheromone);
    free(colony);
    free(paths);
    free(path_lengths);
    return selected_indices;
}

static void write_reduced_csv(const RawCsv *csv, const int *selected_indices,
    int selected_count, const char *output_path) {
    FILE *file = fopen(output_path, "wb");
    int i;

    if (!file) {
        fprintf(stderr, "Erro: nao foi possivel criar '%s'.\n", output_path);
        exit(EXIT_FAILURE);
    }

    fprintf(file, "%s\n", csv->header_line);
    for (i = 0; i < selected_count; i++) {
        int row = selected_indices[i];
        fprintf(file, "%s\n", csv->row_lines[row]);
    }

    fclose(file);
}

static char *output_path_for_seed(const char *base_path, uint32_t seed) {
    const char *last_slash = strrchr(base_path, '/');
    const char *last_backslash = strrchr(base_path, '\\');
    const char *last_separator = last_slash;
    const char *dot = strrchr(base_path, '.');
    char seed_suffix[64];
    size_t prefix_len;
    size_t total_len;
    char *output;

    if (last_separator == NULL || (last_backslash != NULL && last_backslash > last_separator)) {
        last_separator = last_backslash;
    }

    if (dot != NULL && last_separator != NULL && dot < last_separator) {
        dot = NULL;
    }

    snprintf(seed_suffix, sizeof(seed_suffix), "_seed%u", seed);
    prefix_len = dot != NULL ? (size_t)(dot - base_path) : strlen(base_path);
    total_len = prefix_len + strlen(seed_suffix) + (dot != NULL ? strlen(dot) : 4U);

    output = (char *)xmalloc(total_len + 1U);
    memcpy(output, base_path, prefix_len);
    output[prefix_len] = '\0';
    strcat(output, seed_suffix);
    strcat(output, dot != NULL ? dot : ".csv");
    return output;
}

static void print_usage(const char *program) {
    printf("Uso:\n");
    printf("  %s <entrada.csv> [saida.csv] [opcoes]\n\n", program);
    printf("Opcoes:\n");
    printf("  --target <nome|indice>          Coluna de classe; padrao: ultima coluna\n");
    printf("  --seed <inteiro>                Executa uma unica seed\n");
    printf("  --seeds <a,b,c>                 Lista de seeds; padrao: 0,42,123,789,1024\n");
    printf("  --initial-pheromone <valor>     Feromonio inicial; padrao: 1\n");
    printf("  --evaporation-rate <valor>      Taxa de evaporacao; padrao: 0.1\n");
    printf("  --q <valor>                     Fator de deposito; padrao: 1\n");
}

static Config parse_args(int argc, char **argv) {
    Config config;
    int positional = 0;
    int i;

    config.input_path = NULL;
    config.output_path = "reduzido_c.csv";
    config.target_arg = NULL;
    config.initial_pheromone = 1.0;
    config.evaporation_rate = 0.1;
    config.q = 1.0;
    config.seeds[0] = 0U;
    config.seeds[1] = 42U;
    config.seeds[2] = 123U;
    config.seeds[3] = 789U;
    config.seeds[4] = 1024U;
    config.seed_count = 5;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            exit(EXIT_SUCCESS);
        } else if (strcmp(argv[i], "--target") == 0) {
            if (++i >= argc) {
                fprintf(stderr, "Erro: --target exige um valor.\n");
                exit(EXIT_FAILURE);
            }
            config.target_arg = argv[i];
        } else if (strcmp(argv[i], "--seed") == 0) {
            if (++i >= argc) {
                fprintf(stderr, "Erro: --seed exige um valor.\n");
                exit(EXIT_FAILURE);
            }
            config.seeds[0] = parse_seed_strict(argv[i]);
            config.seed_count = 1;
        } else if (strcmp(argv[i], "--seeds") == 0) {
            if (++i >= argc) {
                fprintf(stderr, "Erro: --seeds exige uma lista.\n");
                exit(EXIT_FAILURE);
            }
            parse_seed_list(argv[i], &config);
        } else if (strcmp(argv[i], "--initial-pheromone") == 0) {
            if (++i >= argc || !parse_double_strict(argv[i], &config.initial_pheromone)) {
                fprintf(stderr, "Erro: --initial-pheromone invalido.\n");
                exit(EXIT_FAILURE);
            }
        } else if (strcmp(argv[i], "--evaporation-rate") == 0) {
            if (++i >= argc || !parse_double_strict(argv[i], &config.evaporation_rate)) {
                fprintf(stderr, "Erro: --evaporation-rate invalido.\n");
                exit(EXIT_FAILURE);
            }
        } else if (strcmp(argv[i], "--q") == 0) {
            if (++i >= argc || !parse_double_strict(argv[i], &config.q)) {
                fprintf(stderr, "Erro: --q invalido.\n");
                exit(EXIT_FAILURE);
            }
        } else if (argv[i][0] == '-') {
            fprintf(stderr, "Erro: opcao desconhecida '%s'.\n", argv[i]);
            exit(EXIT_FAILURE);
        } else {
            if (positional == 0) {
                config.input_path = argv[i];
            } else if (positional == 1) {
                config.output_path = argv[i];
            } else {
                fprintf(stderr, "Erro: argumento extra '%s'.\n", argv[i]);
                exit(EXIT_FAILURE);
            }
            positional++;
        }
    }

    if (!config.input_path) {
        print_usage(argv[0]);
        exit(EXIT_FAILURE);
    }
    if (config.evaporation_rate < 0.0 || config.evaporation_rate > 1.0) {
        fprintf(stderr, "Erro: taxa de evaporacao deve estar em [0, 1].\n");
        exit(EXIT_FAILURE);
    }
    return config;
}

int main(int argc, char **argv) {
    Config config = parse_args(argc, argv);
    RawCsv csv;
    Dataset dataset;
    int target_col;
    double *run_times;
    double *total_seed_times;
    int *selected_counts;
    int seed_index;
    clock_t experiment_start = clock();
    clock_t experiment_end;

    csv = read_csv(config.input_path);
    target_col = resolve_target_column(&csv, config.target_arg);
    dataset = build_dataset(&csv, target_col);
    run_times = (double *)xmalloc(sizeof(double) * (size_t)config.seed_count);
    total_seed_times = (double *)xmalloc(sizeof(double) * (size_t)config.seed_count);
    selected_counts = (int *)xmalloc(sizeof(int) * (size_t)config.seed_count);

    printf("Arquivo: %s\n", config.input_path);
    printf("Instancias: %d | Atributos: %d | Classes: %d | Alvo: %s\n",
        dataset.rows, dataset.features, dataset.classes, csv.headers[target_col]);
    printf("Parametros: feromonio inicial=%.6g | evaporacao=%.6g | Q=%.6g\n",
        config.initial_pheromone, config.evaporation_rate, config.q);
    printf("Seeds:");
    for (seed_index = 0; seed_index < config.seed_count; seed_index++) {
        printf("%s%u", seed_index == 0 ? " " : ", ", config.seeds[seed_index]);
    }
    printf("\nIniciando execucoes C\n");

    for (seed_index = 0; seed_index < config.seed_count; seed_index++) {
        uint32_t seed = config.seeds[seed_index];
        int selected_count;
        int *selected_indices;
        double best_accuracy;
        double aco_time;
        double knn_time;
        char *output_path;
        clock_t run_start;
        clock_t run_end;
        clock_t seed_end;

        printf("\nSeed %u\n", seed);
        run_start = clock();
        selected_indices = run_colony(&dataset, config.initial_pheromone,
            config.evaporation_rate, config.q, seed, &selected_count,
            &best_accuracy, &aco_time, &knn_time);
        run_end = clock();

        output_path = config.seed_count > 1 ?
            output_path_for_seed(config.output_path, seed) : xstrdup(config.output_path);
        write_reduced_csv(&csv, selected_indices, selected_count, output_path);
        seed_end = clock();

        run_times[seed_index] = elapsed_seconds(run_start, run_end);
        total_seed_times[seed_index] = elapsed_seconds(run_start, seed_end);
        selected_counts[seed_index] = selected_count;

        printf("Instancias selecionadas: %d\n", selected_count);
        printf("Acuracia 1-NN da melhor solucao: %.6f\n", best_accuracy);
        printf("Tempo ACO: %.6f segundos\n", aco_time);
        printf("Tempo avaliacao 1-NN: %.6f segundos\n", knn_time);
        printf("Tempo run_colony: %.6f segundos\n", run_times[seed_index]);
        printf("Tempo total seed: %.6f segundos\n", total_seed_times[seed_index]);
        printf("CSV reduzido salvo em: %s\n", output_path);

        free(output_path);
        free(selected_indices);
    }

    experiment_end = clock();

    printf("\nResumo C\n");
    printf("Execucoes: %d\n", config.seed_count);
    printf("Tempo medio run_colony: %.6f segundos\n",
        mean_double(run_times, config.seed_count));
    printf("Desvio padrao run_colony: %.6f segundos\n",
        stdev_double(run_times, config.seed_count));
    printf("Tempo medio total por seed: %.6f segundos\n",
        mean_double(total_seed_times, config.seed_count));
    printf("Desvio padrao total por seed: %.6f segundos\n",
        stdev_double(total_seed_times, config.seed_count));
    printf("Instancias selecionadas media: %.2f\n",
        mean_int(selected_counts, config.seed_count));
    printf("Tempo total do experimento: %.6f segundos\n",
        elapsed_seconds(experiment_start, experiment_end));

    free(run_times);
    free(total_seed_times);
    free(selected_counts);
    free_dataset(&dataset);
    free_csv(&csv);
    return EXIT_SUCCESS;
}
