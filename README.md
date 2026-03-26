[English](README.md) | [简体中文](README.zh.md)

agent-skills-connect:

Why connect?

If I currently have Skill A, which automatically identifies uploaded content, saves it, and summarizes it, and Skill B, which automatically collects hot news, creating a new Skill C that saves hot news while extracting technical content seems like the natural next step if I want to achieve both goals simultaneously. But what if I used a method to combine them instead? Reasons:

1) After combining A and B, we can still retain these two prototypes, inspiring our future ideas.
2) More fundamental skills, such as A, can be combined with other new skills to implement richer, localized features.
3) Suppose A and B come from the community and are being continuously improved—for instance, A adds support for more databases or adopts more reasonable database schemas. Their "newborn baby," C, would remain stuck locally and stagnant (its parents are evolving, but it is not).

How to connect?

Well, there are many ways. I mean...

Currently, I can only think of the following methods:

1) Create a new JSON file mentioning A and B, supplemented with descriptions of some necessary new functionalities.
2) Directly modify A and B to give them interface-like capabilities for receiving additional information. However, this contradicts my reason #3 above.
3) ....

As a reference for agent-system-prompt, please refer to [agent-system-prompt.txt](agent-system-prompt.txt).
Please use it as the system prompt for the agent or submit the entire repository file to the agent.
