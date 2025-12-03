# ./main_discussion.py

from provider.open_router import OpenRouter
from provider.model import Model
from orchestrator import Orchestrator
from constants.constants import Model as ModelEnum

# Create council members (no roles, just different models for diversity)
member1 = Model(ModelEnum.OPEN_ROUTER_GEMMA_3_27B_IT.value, OpenRouter)
member2 = Model(ModelEnum.OPEN_ROUTER_GROK_4_1_FAST.value, OpenRouter)
member3 = Model(ModelEnum.OPEN_ROUTER_DEEPSEEK_R1T2_CHIMERA.value, OpenRouter)

# Council head
head = Model(ModelEnum.OPEN_ROUTER_GROK_4_1_FAST.value, OpenRouter)

# Initialize discussion orchestrator
# num_rounds is a requested max, actual max is capped at 3 inside the orchestrator
orchestrator = Orchestrator(
    council_head=head,
    council_members=[member1, member2, member3],
    num_rounds=3,
    member_names=["Gemma", "Grok", "Deepseek"],
)

if __name__ == "__main__":
    # Run autonomous discussion on a complex topic
    # query = "Should AI agents be allowed to make autonomous financial decisions for users?"
    query = "What is the capital of France?"
    result = orchestrator.run_discussion(query)
    
    print("\n" + "="*80)
    print("DISCUSSION COMPLETE")
    print("="*80)
    print(f"Total rounds requested: {result['num_rounds_requested']}")
    print(f"Total rounds executed: {result['num_rounds_executed']}")
    print(f"Stopped early: {result['stopped_early']}")
    print(f"Final decision available: {result['final_decision'] is not None}")
