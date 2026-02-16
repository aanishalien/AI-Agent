from app.agents.decision_maker import decide_action
from app.tools.calculator import calculate
from app.tools.file_reader import read_file
from app.tools.web_search import web_search
from app.agents.reasoner import generate_final_answer
from app.agents.planner import create_plan
from app.memory.short_memory import ShortTermMemory
from app.memory.long_memory import LongTermMemory
from app.agents.reflection import reflect_answer
from app.agents.monitor import AgentMonitor
from app.agents.tool_summarizer import summarize_tool_output


monitor = AgentMonitor()
stm = ShortTermMemory()
ltm = LongTermMemory()


def run_agent(user_query: str):
    print("\nThinking...\n")

    stm.add("user", user_query)

    # 🧠 Create plan
    plan = create_plan(user_query, stm.get_context(), ltm.recall())
    print("\n[PLAN]")
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")

    tool_result = None
    max_steps = 5

    # 🔁 Execute each step from planner
    for step_index, step_instruction in enumerate(plan):

        if monitor.should_stop(step_index,max_steps):
            return "Stopped: Too many steps without resolution."
        
        context = stm.get_context()
        facts = ltm.recall()

        print(f"\n[Executing Step {step_index+1}] {step_instruction}")

        decision = decide_action(step_instruction)

        if not decision.get("use_tool"):
            continue

        tool_name = decision.get("tool_name")
        tool_input = decision.get("tool_input")

        if monitor.is_repeating_tool(tool_name, tool_input):
            return "Stopped: Repeated tool usage detected."
        

        print(f"Using tool: {tool_name}")
        print(f"Tool input: {tool_input}")

        try:
            if tool_name == "calculator":
                tool_result = calculate(tool_input)

            elif tool_name == "file_reader":
                tool_result = read_file(tool_input)

            elif tool_name == "web_search":
                tool_result = web_search(tool_input)

            else:
                return "Unknown tool selected."

        except Exception as e:
            return f"Tool Error: {str(e)}"
        
        summary = summarize_tool_output(user_query,tool_result)

        print("\n[TOOL SUMMARY]\n", summary)
        
        monitor.log_step(tool_name, tool_input, summary)

        stm.add("tool_summary", summary)

        if step_index >= 2 and tool_result:
            print("Sufficent data collected.Breaking research loop.")
            break
        
        if monitor.no_new_information():
            return "Stopped: No new information gained"

    # 🧠 Final reasoning AFTER plan execution
    final_answer = generate_final_answer(
        user_query,
        tool_result,
        stm.get_context(),
        ltm.recall()
    )

    reflection = reflect_answer(final_answer, tool_result,user_query)
    print("\n[REFLECTION]",reflection)

    if not reflection.retry_needed:
        print("Reflection says answer may be wrong. Retry tools or reasoning.")

    print("\nRetrying with improved reasoning...\n")
    stm.add("assistant", final_answer)

    if "remember" in user_query.lower():
        ltm.remember(user_query)

    return final_answer


