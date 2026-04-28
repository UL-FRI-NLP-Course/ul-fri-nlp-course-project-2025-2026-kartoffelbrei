from dataclasses import dataclass

@dataclass
class PromptBuilder:
    task: str
    schema: str
    rules: str
    examples: str

    def build(self, user_input: str) -> str:
        return f"""
        ### TASK
        {self.task}

        ### OUTPUT
        Return ONLY valid JSON.
        
        ### SCHEMA
        {self.schema}
        
        ### RULES
        {self.rules}
        
        ### EXAMPLES
        {self.examples}
        
        ### INPUT
        User: {user_input}
        Output:
        """

#todo: find right format for departure date
intent_prompt_builder = PromptBuilder(
    task="Extract structured data from a railway query.",

    schema="""
    {
    "intent": "train information | arrival | departure | route | other",
    "train_number": string or null,
    "departure_station": string or null,
    "destination_station": string or null,
    "departure_date": date or null,
    
    "needs_api": boolean
    }
    """,

    rules="""
    - Do not explain
    - Do not output anything except JSON
    - Use null if unknown
    - needs_api = true for real-time queries
    """,

    examples="""
    User: Is IC 46 delayed today?
    Output:
    {"intent":"delay","train_type":"IC","train_number":"46","departure_station":null,"destination_station":null,"needs_api":true}
    """
)