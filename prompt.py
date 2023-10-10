import json
from random import shuffle
 
# INSTRUCTION = """Note: The following debate transcript may contain imperfections, such as multiple people talking over each other and question being asked by indivudals or moderator. Please take this into consideration when analyzing the text.
# Analyze the following debate excerpt for logical fallacies and format your response by starting with the name of the fallacy, followed by a brief justification.
# If the statement is factual or logical, or if no argument is present, state so explicitly. Avoid covering the same points from the Last Debate Excerpt.

# Debate Excerpt: 
# """

INSTRUCTION = """Note: The following debate transcript may contain imperfections, such as multiple people talking over each other and questions being asked by individuals or the moderator. Please take this into consideration when analyzing the text.
Analyze the following debate excerpt for logical fallacies based on the pragma-dialectical framework:

1.Argumentum ad Hominem (Personal Attack)
- Identify this when the speaker attacks the character, motive, or other attributes of the person making the argument, rather than attacking the substance of the argument itself.

2. Argumentum ad Populum (Appeal to Popular Opinion)
- Look for claims that are justified solely because "everyone else believes it" or "it is popular."

3. Argumentum ad Ignorantiam (Appeal to Ignorance)
- Spot this fallacy when the argument asserts that a proposition is true because it has not been proven false, or vice versa.

4. Argumentum ad Misericordiam (Appeal to Pity)
- Identify when emotional appeals like sympathy, pity, or fear are used instead of logical reasons to persuade the audience.

5. Argumentum ad Baculum (Appeal to Force)
- Notice when threats or force are used to win an argument, rather than logic or evidence.

6. Slippery Slope
- Look out for claims that one event will inevitably follow from another without adequate evidence to support such a claim.

7. False Dichotomy
- Identify when only two choices are presented as the only options, while in reality, more options exist.

8. Begging the Question (Circular Reasoning)

- Recognize this when the conclusion is already assumed in the premises, essentially forming a circle in reasoning.

9. Straw Man Fallacy
- Look for instances where an argument is misrepresented to make it easier to attack.

10. Red Herring
- Identify when the argument goes off on a tangent, providing irrelevant information to distract from the main issue.

11. Hasty Generalization
- Notice when conclusions are drawn based on insufficient or unrepresentative evidence.

12. Equivocation
- Look for ambiguous language that can be interpreted in more than one way, used intentionally to mislead or confuse.

Justification for classification of the statement as that fallacy, claim that is impacted by the fallacy, severity of the damage done to the claim by presence of that fallacy with column labels: name, justification, claim, damage. If the statement is factual or logical, or if no argument is present, state so explicitly. Avoid covering the same points from the Last Debate Excerpt.

Debate Excerpt:
"""


def get_few_shot_examples(file_name=r'Data/data.json', N=5):
    try:
        with open(file_name, "r") as json_file:
            all_data = json.load(json_file)
    except FileNotFoundError:
        return "No data available."
    
    shuffle(all_data)
    # Get last N examples from the JSON data
    last_n_examples = all_data[-N:]
    
    # Generate the few-shot string
    few_shot_string = ""
    for example in last_n_examples:
        few_shot_string += f"Debate Excerpt: \"{example['transcript']}\"\n"
        few_shot_string += f"{example['response']}\n\n"
    
    return few_shot_string


def get_prompt(transcript, last_responce):
    few_shot = get_few_shot_examples(file_name=r'Data/data.json', N=5)
    
    prompt = f'{few_shot}\n{last_responce}\n\n{INSTRUCTION}\n\"{transcript}\"'
    return prompt

if __name__=="__main__":
    pass
    # update_json_file( file_name=r'Data/data.json')