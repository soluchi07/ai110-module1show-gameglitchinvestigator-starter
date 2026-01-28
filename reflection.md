# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - it was an interface that asked you to guess a number between 0 and 100
  - you keep putting in number and clicking guess to submit the guess
  - press new game to start a new game and hint checkbox to toggle hints 

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  - the new game button didnt work and a new game didnt start
  - it didnt give me all the attempts i had left (says ive used 8 attempt when i only used 7) or tells me the wrong number of attempts i have when i start a new game
  - hints are backwards

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Copilot especially the Agent Mode
- Give one example of an AI suggestion you accepted and why.
  - Copilot suggested using `st.session_state` to store the secret number so it wouldn't regenerate on every rerun. I accepted this because it directly solved the core bug where the number kept changing.

- Give one example of an AI suggestion you changed or rejected and why.
  - Copilot suggested rewriting the entire hints logic, but I rejected that and only flipped the comparison operators instead. The original structure was clear enough, and a minimal fix was safer than rewriting working code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I ran the game manually multiple times, playing through guesses without clicking "New Game" to verify the secret number stayed the same. I also tested the "New Game" button to confirm it actually reset properly. When all three bugs showed different behavior than before, I knew the fixes worked.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - I ran a test using pytest to check the functionality of the `check_guess` function. This test confirmed that the function returned the correct outcomes for various inputs, ensuring that the game logic was sound and that the hints provided were accurate based on the player's guesses.
  - I learned that thorough testing, both manual and automated, is crucial for maintaining the integrity of the game and providing a smooth user experience.
  - I plan to implement more automated tests in future projects to catch bugs early and ensure that changes do not introduce new issues.
  - I now view AI as a collaborative partner that can assist in the coding process, but I remain responsible for understanding and validating the suggestions it provides.

- Did AI help you design or understand any tests? How?
  - Yes, Copilot explained how `st.session_state` works and suggested printing debug values to verify the state was being saved. That helped me understand what to look for when testing.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - Every time Streamlit reruns the script (which happens on every user interaction), any variable that generates a random number gets recalculated. Without storing it in session state, the secret number would be a new random value each rerun.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Streamlit reruns your entire Python script from top to bottom whenever the user interacts with the app. Session state is like a sticky note that persists across reruns, so variables stored there don't get reset.

- What change did you make that finally gave the game a stable secret number?
  I wrapped the secret number initialization in an `if` statement that checks `st.session_state`, so it only generates once when the app first loads and stores it. On subsequent reruns, it retrieves the stored value instead of recalculating.
  

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - Testing my code manually by actually using the app like a real user rather than just reading the code. It caught bugs that code review alone would have missed.

- What is one thing you would do differently next time you work with AI on a coding task?
  - I'd ask the AI to explain *why* a fix works before accepting it, instead of just trusting it blindly. Understanding the reasoning would have made the session state concept click faster.
  -I will also try to practice using a new chat for each new task so the AI doesn't lose context

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI suggestions are starting points, not gospel. The best approach was combining AI's domain knowledge with my own testing and judgment to find minimal, safe fixes.