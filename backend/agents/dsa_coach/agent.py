import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools.leetcode_tool import get_practice_problems

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Describe the tool so the model knows it exists and how to call it
get_practice_problems_declaration = {
    "name": "get_practice_problems",
    "description": "Returns a list of recommended LeetCode practice problems for a given DSA topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The DSA topic to get practice problems for, e.g. 'dynamic programming', 'graphs', 'arrays'."
            }
        },
        "required": ["topic"]
    }
}

tools = types.Tool(function_declarations=[get_practice_problems_declaration])
config = types.GenerateContentConfig(tools=[tools])


def coach_on_topic(weak_topic: str) -> dict:
    user_message = f"""I'm weak in {weak_topic} for coding interviews. Can you recommend some
practice problems and give me a short tip on how to approach this topic?"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user_message,
        config=config
    )

    function_call = response.candidates[0].content.parts[0].function_call

    if function_call and function_call.name == "get_practice_problems":
        topic_arg = function_call.args["topic"]
        problems = get_practice_problems(topic_arg)

        # Send the tool's result back to the model to get its final answer
        follow_up = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[
                user_message,
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name="get_practice_problems",
                        response={"problems": problems}
                    )]
                )
            ],
            config=config
        )

        return {
            "topic": weak_topic,
            "problems_recommended": problems,
            "coaching_advice": follow_up.text
        }

    # Fallback: model answered directly without calling the tool
    return {
        "topic": weak_topic,
        "problems_recommended": [],
        "coaching_advice": response.text
    }
