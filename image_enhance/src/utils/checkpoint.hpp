// checkpoint.hpp - Save and load model weights
#ifndef CHECKPOINT_HPP
#define CHECKPOINT_HPP

#include <cstdio>
#include <cstdlib>
#include <string>

// Save weights to binary file
inline void save_weights(const char* path, float* weights, size_t size) {
    FILE* f = fopen(path, "wb");
    if (!f) {
        fprintf(stderr, "Error: Cannot open file %s for writing\n", path);
        return;
    }
    fwrite(&size, sizeof(size_t), 1, f);      // Save size first
    fwrite(weights, sizeof(float), size, f);  // Save weights
    fclose(f);
    printf("Saved %zu weights to %s\n", size, path);
}

// Load weights from binary file
inline void load_weights(const char* path, float* weights, size_t& size) {
    FILE* f = fopen(path, "rb");
    if (!f) {
        fprintf(stderr, "Error: Cannot open file %s for reading\n", path);
        return;
    }
    fread(&size, sizeof(size_t), 1, f);       // Read size
    fread(weights, sizeof(float), size, f);   // Read weights
    fclose(f);
    printf("Loaded %zu weights from %s\n", size, path);
}

#endif // CHECKPOINT_HPP
