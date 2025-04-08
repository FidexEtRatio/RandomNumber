#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    const unsigned int count = 990773;
    unsigned short num;

    FILE *file = fopen("prng_data2.bin", "wb");
    if (!file) {
        perror("Failed to open file");
        return 1;
    }

    long int start = time(NULL);

    for (unsigned int i = 0; i < count; i++) {
        num = rand() % 65536;
        printf("Generated number %d/%d\n", i + 1, count);
        
        unsigned char bytes[2];
        bytes[0] = (num >> 8) & 0xFF;
        bytes[1] = num & 0xFF;        

        fwrite(bytes, sizeof(unsigned char), 2, file);
    }

    // End timing
    unsigned long end = time(NULL);
    double duration = end - start;
    double rate = count / duration;

    fclose(file);

    printf("Generated and wrote %u numbers in %.4f seconds\n", count, duration);
    printf("Rate: %.0f numbers/second\n", rate);

    return 0;
}
