# ./discussion_orchestrator.py

from provider.model import Model
from typing import List, Dict
from prompts.prompts import (
    DISCUSSION_ROUND_1_PROMPT,
    DISCUSSION_ROUND_N_PROMPT,
    COUNCIL_HEAD_DISCUSSION_PROMPT
)
from utils.logger import setup_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

logger = setup_logger("discussion")


class Orchestrator:
    """Orchestrates autonomous multi-round discussions between council members."""
    
    def __init__(
        self, 
        council_head: Model, 
        council_members: List[Model],
        num_rounds: int = 3,
        member_names: List[str] = None
    ):
        """
        Args:
            council_head: Model that makes final decision
            council_members: List of models that participate in discussion
            num_rounds: Desired number of discussion rounds
            member_names: Optional names for members (default: Member 1, Member 2, ...)
        """
        # Enforce a max of 3 rounds
        self.num_rounds = min(num_rounds, 3)

        self.council_head = council_head
        self.council_members = council_members
        self.member_names = member_names or [f"Member {i+1}" for i in range(len(council_members))]
        self.discussion_history: List[Dict] = []
        
        logger.info(
            f"Initialized discussion orchestrator with "
            f"{len(council_members)} members, requested rounds={num_rounds}, "
            f"using num_rounds={self.num_rounds} (max 3)"
        )

    def _extract_content(self, response: dict) -> str:
        """Extract content from different provider response formats."""
        if not response:
            return ""
        if "choices" in response:
            return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        return response.get("message", {}).get("content", "")

    def _get_member_response(
        self, 
        member: Model, 
        member_name: str,
        messages: List[dict]
    ) -> tuple:
        """Get response from a single member with error handling."""
        try:
            logger.info(f"{member_name} starting response...")
            start_time = time.time()
            
            response = member.generate(messages)
            content = self._extract_content(response)
            
            elapsed = time.time() - start_time
            logger.info(f"{member_name} completed in {elapsed:.2f}s")
            
            return content, None
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"{member_name} failed: {error_msg}", exc_info=True)
            return None, error_msg

    def _format_discussion_history(self, up_to_round: int = None) -> str:
        """Format discussion history for context."""
        if up_to_round is None:
            up_to_round = len(self.discussion_history)
        
        formatted = ""
        for round_data in self.discussion_history[:up_to_round]:
            round_num = round_data["round"]
            formatted += f"\n{'='*80}\n"
            formatted += f"ROUND {round_num}\n"
            formatted += f"{'='*80}\n\n"
            
            for response in round_data["responses"]:
                name = response["name"]
                content = response["content"]
                formatted += f"--- {name} ---\n{content}\n\n"
        
        return formatted

    def _should_stop_early(self, round_responses: List[Dict]) -> bool:
        """
        Agents can request early stop by returning a special keyword.
        
        Protocol for the models (put this in your prompts):
          If you believe the discussion has converged or is ready for a final decision,
          include the phrase READY_FOR_DECISION somewhere in your reply.
          
          If you believe the discussion should stop immediately,
          include the phrase STOP_DISCUSSION somewhere in your reply.
        """
        for r in round_responses:
            content = r["content"].strip().lower()
            if "stop_discussion" in content:
                logger.info(f"{r['name']} requested STOP_DISCUSSION")
                return True
            if "ready_for_decision" in content:
                logger.info(f"{r['name']} requested READY_FOR_DECISION")
                return True
        return False

    def _run_discussion_round(self, round_number: int, query: str):
        """Execute a single discussion round with all members."""
        logger.info(f"Starting Round {round_number}")
        
        print(f"\n{'='*80}")
        print(f"ROUND {round_number}")
        print(f"{'='*80}\n")
        
        # Build messages for this round
        if round_number == 1:
            # First round, initial positions
            system_prompt = DISCUSSION_ROUND_1_PROMPT
            user_content = f"Query: {query}"
        else:
            # Subsequent rounds debate with history
            discussion_so_far = self._format_discussion_history(round_number - 1)
            system_prompt = DISCUSSION_ROUND_N_PROMPT.format(
                discussion_history=discussion_so_far,
                round_number=round_number
            )
            user_content = (
                f"Original Query: {query}\n\n"
                f"Continue the discussion based on the above debate. "
                f"If you believe the council is ready for a final decision, "
                f"include READY_FOR_DECISION. "
                f"If you believe the discussion should stop now, include STOP_DISCUSSION."
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        
        # Collect responses from all members in parallel
        round_responses: List[Dict] = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=len(self.council_members)) as executor:
            future_to_member = {
                executor.submit(
                    self._get_member_response,
                    member,
                    self.member_names[idx],
                    messages
                ): (member, self.member_names[idx], idx)
                for idx, member in enumerate(self.council_members)
            }
            
            results = []
            for future in as_completed(future_to_member):
                _, name, idx = future_to_member[future]
                content, error = future.result()
                results.append((idx, name, content, error))
            
            # Sort by original index to keep member ordering
            results.sort(key=lambda x: x[0])
        
        elapsed = time.time() - start_time
        logger.info(f"Round {round_number} completed in {elapsed:.2f}s")
        
        # Display and store responses
        for idx, name, content, error in results:
            print(f"{'─'*80}")
            print(f"{name}:")
            print(f"{'─'*80}")
            
            if error:
                print(f"⚠️  {error}")
                logger.warning(f"{name} failed in round {round_number}")
            else:
                print(content)
                round_responses.append(
                    {
                        "name": name,
                        "content": content,
                    }
                )
            print()
        
        # Store round in history
        self.discussion_history.append(
            {
                "round": round_number,
                "responses": round_responses,
            }
        )

        # Early stop logic based on member signals
        if round_responses and self._should_stop_early(round_responses):
            logger.info(f"Round {round_number} requested early stop")
            return "EARLY_STOP"
        
        # Return False if no successful responses, True otherwise
        return len(round_responses) > 0

    def _get_head_decision(self, query: str):
        """Get final decision from council head based on full discussion."""
        logger.info("Council head making final decision...")
        
        print(f"\n{'='*80}")
        print("🎯 COUNCIL HEAD FINAL DECISION")
        print(f"{'='*80}\n")
        
        full_discussion = self._format_discussion_history()
        
        messages = [
            {
                "role": "system",
                "content": COUNCIL_HEAD_DISCUSSION_PROMPT.format(
                    num_rounds=len(self.discussion_history),
                    full_discussion=full_discussion
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original Query: {query}\n\n"
                    f"Provide your final decision based on the discussion above. "
                    f"If you think more rounds were needed, mention that in your reasoning, "
                    f"but still provide the best possible decision now."
                ),
            },
        ]
        
        try:
            start_time = time.time()
            response = self.council_head.generate(messages)
            content = self._extract_content(response)
            elapsed = time.time() - start_time
            
            logger.info(f"Head decision completed in {elapsed:.2f}s")
            
            print(content)
            print(f"\n{'='*80}\n")
            
            return content
        except Exception as e:
            logger.error(f"Head decision failed: {str(e)}", exc_info=True)
            print(f"❌ Error: Council head failed to make decision: {str(e)}")
            return None

    def run_discussion(self, query: str) -> dict:
        """
        Run full autonomous discussion with multiple rounds and final decision.
        
        Agents are allowed to:
          • Stop the discussion early using STOP_DISCUSSION
          • Signal readiness for a decision using READY_FOR_DECISION
        
        The orchestrator will:
          • Respect early stop signals from any member
          • Never exceed self.num_rounds, which is capped at 3
        
        Args:
            query: The topic or question for discussion
            
        Returns:
            dict with:
                'query'
                'final_decision'
                'discussion_history'
                'num_rounds_requested'
                'num_rounds_executed'
                'stopped_early'
        """
        logger.info(f"Starting autonomous discussion: {query[:100]}...")
        
        print("="*80)
        print(f"QUERY: {query}")
        print("="*80)
        print(
            f"\nStarting discussion with up to {self.num_rounds} rounds "
            f"and {len(self.council_members)} members...\n"
        )
        
        self.discussion_history = []
        
        early_stop = False
        rounds_executed = 0
        
        # Run discussion rounds
        for round_num in range(1, self.num_rounds + 1):
            result = self._run_discussion_round(round_num, query)
            rounds_executed = round_num

            if result == "EARLY_STOP":
                early_stop = True
                print(f"\nAgents ended discussion after round {round_num}")
                break

            if not result:
                logger.warning(f"Round {round_num} had no successful responses")

        # Get final decision from head
        final_decision = self._get_head_decision(query)
        
        result = {
            "query": query,
            "final_decision": final_decision,
            "discussion_history": self.discussion_history,
            "num_rounds_requested": self.num_rounds,
            "num_rounds_executed": rounds_executed,
            "stopped_early": early_stop,
        }
        
        logger.info(
            f"Discussion completed. Executed {rounds_executed} rounds, "
            f"early_stop={early_stop}"
        )
        return result
