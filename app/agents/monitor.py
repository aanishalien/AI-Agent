class AgentMonitor:
    def __init__(self):
        self.tool_history = []
        self.results_history = []
        self.max_repeats = 2

    def log_step(self,tool_name, tool_input, result):
        self.tool_history.append((tool_name, tool_input))
        self.results_history.append(str(result)[:200])
    
    def is_repeating_tool(self, tool_name, tool_input):
        return self.tool_history.count((tool_name, tool_input)) >= self.max_repeats
    
    def no_new_information(self):
        if len(self.results_history) < 2:
            return False
        return self.results_history[-1] == self.results_history[-2]
    
    def should_stop(self, step_count, max_steps):
        return step_count >= max_steps