#include "pmsis.h"
#include "bsp/bsp.h"
#include "cpx.h"

void start_example(void) {
    pi_bsp_init();
    cpxInit();

    int counter = 0;
    while (1) {
        cpxPrintToConsole(LOG_TO_CRTP, "Hello Denise %d!\n", counter);
        counter++;
        pi_time_wait_us(1000*1000);
    }
}

int main(void) {
    return pmsis_kickoff((void *)start_example);
}
