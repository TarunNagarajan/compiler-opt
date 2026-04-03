import time
import sys
from colorama import init, Fore, Back, Style

init(autoreset=True)

def print_step(title, content, delay=1.5):
    print(Fore.CYAN + Style.BRIGHT + f"\n=== {title} ===" + Style.RESET_ALL)
    for line in content:
        print(line)
        time.sleep(0.4)
    time.sleep(delay)

print(Fore.MAGENTA + Style.BRIGHT + "\n>>> HRL AGENT & WORLD MODEL INTERACTION TRACE <<<\n" + Style.RESET_ALL)
print("Target: " + Fore.YELLOW + "nested_loop_0042.c" + Style.RESET_ALL)
print("Goal: Minimum Execution Runtime\n")

time.sleep(1)

print_step("STEP 1: ENVIRONMENT OBSERVATION", [
    f"1. {Fore.GREEN}CompilerOptEnv{Style.RESET_ALL} parses LLVM IR into a Graph.",
    f"2. Graph Size: 420 Nodes, 512 Edges.",
    f"3. {Fore.GREEN}Telescopic GNN Encoder{Style.RESET_ALL} condenses the graph into a 128-dim Latent State (Z_t)."
])

print_step("STEP 2: HRL MANAGER PROPOSES ACTIONS", [
    f"1. The {Fore.BLUE}HRL Manager Policy{Style.RESET_ALL} receives Z_t.",
    f"2. Analyzing current context against past mathematical patterns...",
    f"3. Manager selects Top-3 candidate Macro Actions:",
    f"   - Candidate A: {Fore.YELLOW}Macro[10]{Style.RESET_ALL} ['SROA', 'SLP-Vectorizer'] (confidence: 65%)",
    f"   - Candidate B: {Fore.YELLOW}Macro[1]{Style.RESET_ALL} ['GVN', 'InstCombine'] (confidence: 25%)",
    f"   - Candidate C: {Fore.YELLOW}Macro[14]{Style.RESET_ALL} ['SROA', 'IndVars'] (confidence: 10%)"
])

print_step("STEP 3: WORLD MODEL SIMULATION (Mental Sandbox)", [
    f"1. The {Fore.MAGENTA}World Model{Style.RESET_ALL} spins up to evaluate the candidates WITHOUT running LLVM.",
    f"2. Simulating Candidate A (['SROA', 'SLP-Vectorizer']):",
    f"   - Predicting next Latent State (Z_t+1)...",
    f"   - Predicting execution cost... {Fore.RED}High memory spill probability detected!{Style.RESET_ALL}",
    f"   - Predicted Reward: -0.15",
    f"3. Simulating Candidate C (['SROA', 'IndVars']):",
    f"   - Predicting next Latent State (Z_t+1)...",
    f"   - Predicting execution cost... Exposes clean induction variables.",
    f"   - Predicted Reward: {Fore.GREEN}+0.22{Style.RESET_ALL}"
])

print_step("STEP 4: HRL WORKER REFINEMENT (Micro-Tuning)", [
    f"1. Based on the World Model's advice, {Fore.BLUE}Manager{Style.RESET_ALL} selects Candidate C: Macro[14].",
    f"2. The {Fore.BLUE}HRL Worker (MicroRefiner){Style.RESET_ALL} receives the choice.",
    f"3. Worker inspects the specific loop bounds in Z_t.",
    f"4. Worker Tune: Modifies ['SROA', 'IndVars'] -> {Fore.YELLOW}['SROA', 'IndVars', 'Loop-Unroll<4>']{Style.RESET_ALL}",
    f"   (Reasoning: Known bounded loop of size 16 perfectly divisible by 4)"
])

print_step("STEP 5: EXECUTION & FEEDBACK LOOP", [
    f"1. {Fore.GREEN}CompilerOptEnv{Style.RESET_ALL} applies the refined sequence to the real LLVM IR.",
    f"2. Actual LLVM compilation and profiling occurs.",
    f"3. Real Reward: {Fore.GREEN}+0.24{Style.RESET_ALL} (Runtime dropped 12ms -> 9.1ms).",
    f"4. {Fore.MAGENTA}World Model Update{Style.RESET_ALL}:",
    f"   - Compares its prediction (+0.22) with reality (+0.24).",
    f"   - Adjusts transition weights (Loss: 0.0004).",
    f"5. {Fore.BLUE}HRL Policies Update{Style.RESET_ALL}:",
    f"   - Critic reinforces the path.",
    f"   - Manager increases probability of calling Macro[14] for similar graphs.",
    f"   - Worker is rewarded for injecting 'Loop-Unroll<4>'."
])

print(Fore.WHITE + Style.BRIGHT + "==> CYCLE COMPLETE. Preparing for next optimization step..." + Style.RESET_ALL)
print("\nSimulation complete.")
