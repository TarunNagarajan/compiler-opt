#include <windows.h>
#include <iostream>
#include <string>
#include <vector>

/**
 * Super-Harness v1.0 (Windows)
 * 
 * Objective: Zero-Noise Cycle Measurement for HRL Rewards.
 * Primitives:
 * 1. SetProcessAffinityMask (Core 1)
 * 2. SetPriorityClass (HIGH_PRIORITY_CLASS)
 * 3. QueryProcessCycleTime (Deterministic CPU Cycles)
 */

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: super_harness.exe <benchmark_exe> [args...]" << std::endl;
        return 1;
    }

    // 1. Create the child process in suspended state
    std::string commandLine = "";
    for (int i = 1; i < argc; ++i) {
        commandLine += argv[i];
        if (i < argc - 1) commandLine += " ";
    }

    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    if (!CreateProcessA(NULL, (LPSTR)commandLine.c_str(), NULL, NULL, FALSE, 
                       CREATE_SUSPENDED | IDLE_PRIORITY_CLASS, NULL, NULL, &si, &pi)) {
        std::cerr << "CreateProcess failed (" << GetLastError() << ")" << std::endl;
        return 1;
    }

    // 2. Apply Stability Primitives to Child
    // Pin to Core 1 (Avoid Core 0)
    DWORD_PTR processAffinityMask = 2; // Binary 0010 (Core 1)
    SetProcessAffinityMask(pi.hProcess, processAffinityMask);

    // Set Priority to High
    SetPriorityClass(pi.hProcess, HIGH_PRIORITY_CLASS);

    // 3. Measure Cycles
    ULONG64 cyclesStart, cyclesEnd;
    
    // Resume execution
    ResumeThread(pi.hThread);
    
    // Wait for completion
    WaitForSingleObject(pi.hProcess, INFINITE);

    // Query consumed cycles for the whole process tree
    if (!QueryProcessCycleTime(pi.hProcess, &cyclesEnd)) {
        std::cerr << "QueryProcessCycleTime failed" << std::endl;
        TerminateProcess(pi.hProcess, 1);
        return 1;
    }

    // Output only the metric for the Python parent
    std::cout << "\n[HARNESS_CYCLES] " << cyclesEnd << std::endl;

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
