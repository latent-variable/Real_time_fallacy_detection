import openai  # Assuming you've installed the OpenAI Python package
from local_llm import local_llm_call

# Function to read API key from a file
def read_api_key(file_path = r'./api_key.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
# Initialize GPT-3 API Client
openai.api_key = read_api_key()


def fallacy_classification(text, run_local =True):
     # Create a more nuanced prompt for ChatGPT
    prompt = f"""In the following debate excerpt, identify any logical fallacies by starting with the name of the fallacy, followed by a brief justification. 
    If the statement is factual or logical, or if no argument is present, state so explicitly. 
    Keep your response concise.

    Debate Excerpt: "I have been for border security for years. I voted for border security in the United States.
    State Senate. And my comprehensive immigration reform plan, of course, includes border
    security. But I want to put our resources where I think they're most needed.
    getting rid of any violent person, anybody who should be deported.
    When it comes to the wall that Donald talks about building, he went to the building.
    to Mexico. We had a meeting with the Mexican president. Didn't even raise it. He choked.
    and then got into a Twitter war because the Mexican president said, we're not paying for that wall.
    I think we are both a nation of immigrants and we are a nation of laws and that we can
    and act accordingly. And that's why I'm introducing comprehensive immigration reform."

    Valid Argument - The speaker outlines their stance on border security and immigration reform, citing past voting history and plans for resource allocation. The argument is focused on a balanced approach that includes both border security and humane treatment of immigrants. The speaker also critiques the opponent's approach, pointing out inconsistencies in actions and statements. No fallacy is present.

    Debate Excerpt: "very unfair to all of the people that are waiting in line for many, many years. We need strong borders.
    In the audience tonight, we have four mothers of — I mean —
    These are unbelievable people that I've gotten to know over a period of years whose children have been killed.
    brutally killed by the people that came into the country illegally. You have thousands of mothers.
    and fathers and relatives all over the country. They're coming in illegally.
    drugs are pouring in through the border. We have no country if we have no border. Hillary wants to give out.
    amnesty. She wants to have open borders. The border secure, as you know, the Border Patrol agents.
    and 16,500 plus ICE last week endorsed me. First time they've ever.
    to a sick candidate. It means their job is tougher, but they know what's going on.
    They know it better than anybody. They want strong borders. They feel we have to have strong borders."

    Appeal to Emotion & Anecdotal Evidence - The speaker uses the emotional stories of mothers whose children were killed to argue for stronger borders, rather than providing statistical evidence to support the claim. While the stories are impactful, they are not sufficient to generalize about the overall issue of border security or immigration policy. The speaker also claims that "drugs are pouring in" and attributes endorsements from Border Patrol and ICE as evidence, which could be considered appeals to authority. These tactics divert from a logical, evidence-based discussion on the subject.

    Debate Excerpt: "There can be regulations on abortion so long as the law is in place.
    life and the health of the mother are taken into account.
    I voted as a senator. I did not think that that was the case. The time.
    The kinds of cases that fall at the end of pregnancy are often the most...
    heartbreaking, painful decisions for families to make. I have met—
    with women who, toward the end of their pregnancy...
    Get the worst news one could get that their health is in jeopardy if they continue to get it.
    carried to term or that something terrible has happened or just been discovered.
    about the pregnancy. I do not think the United States government should be step–
    and making those most personal of decisions."

    Valid Argument - Valid Argument - The speaker argues for regulations on abortion that take into account the life and health of the mother. The argument is supported by examples of difficult situations that families might face at the end of pregnancy. The speaker asserts that government should not intervene in these highly personal decisions, providing a logical basis for their stance. No fallacy is present.

    Debate Excerpt: "underpaid undocumented workers and when they complained, he basically said what a lot of employees
    lawyers do. You complain, I'll get you deported. I want to get everybody out of the house.
    the shadows, get the economy working, and not let employers like Donald exploit on Donald.
    documented workers which hurts them but also hurts American workers.
    has moved millions of people out. Nobody knows about it. Nobody talks about it. But under Obama...
    millions of people have been moved out of this country, they've been deported. She doesn't want to say that, but that's what's-
    happened and that's what's happened big league. As far as moving these people out...
    and moving. We either have a country of... We're a country of laws. We either have a border or...
    we don't. Now, you can come back in and you can become a citizen, but it's very...
    unfair. We have millions of people that did it the right way. They were on line. They were waiting."

    Ad Hominem & Strawman - The first speaker accuses the opponent of exploiting undocumented workers, using it as an attack on the opponent's character rather than focusing on the issue of immigration policy. The second speaker claims that "millions of people have been moved out" under the previous administration but implies that the first speaker is unwilling to acknowledge this, creating a strawman argument. Both speakers divert from a constructive, evidence-based discussion on immigration policy.


    Analyze the following debate excerpt for logical fallacies and format your response by starting with the name of the fallacy, followed by a brief justification.
    If the statement is factual or logical, or if no argument is present, state so explicitly. 
    Keep your response concise.

    Debate Excerpt: "{text}"
    """
    print('Propmting GPT')
    # Call ChatGPT API for fallacy detection or other tasks
    if run_local:
        return local_llm_call(prompt)
    else:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
    
    gpt3_output = response['choices'][0]['message']['content'].strip() # Extract and clean the output text
    # print("GPT-3 Output:", gpt3_output)
    return gpt3_output


def is_a_complete_statement(text):
     
    # Create a prompt for ChatGPT to assess the completeness of the statement
    prompt = f"""
    Analyze the following statement from a debate to determine if it contains at least one complete arguments within:
    "{text}"

    Only respond with 'Contains complete arguments' or 'The statement is incomplete'.
    """
    
    # Call ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        
    )
    
    gpt3_output = response['choices'][0]['message']['content'].strip()
    print("GPT-3 Output:", gpt3_output)

    # Further logic based on GPT-3 output
    if " complete" in gpt3_output:
        print("The statement is complete.")
        return True
        # Proceed with fallacy detection or other tasks
    elif "incompleted" in gpt3_output:
        print("The statement is incomplete.")
        return False
    else:
        print('is_a_complete_statement fail')
        return False