#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int distanceBetweenBusStops(int *distance, int distanceSize, int start,
                            int destination)
{
    int sum1 = 0, sum2 = 0;
    if (start > destination)
    {
        int tmp = start;
        start = destination;
        destination = tmp;
    }
    for (auto i = 0; i < distanceSize; ++i)
    {
        if (i >= start && i < destination)
            sum1 += distance[i];
        else
            sum2 += distance[i];
    }
    return sum1 < sum2 ? sum1 : sum2;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = distanceBetweenBusStops(42, 42, 42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
