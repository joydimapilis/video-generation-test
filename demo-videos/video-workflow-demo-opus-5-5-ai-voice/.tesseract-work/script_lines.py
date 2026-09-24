"""The supplied script, verbatim, split into sentences. `say` is the text sent to the
voice model; it differs from `text` only where pronunciation needs a hint."""
STEPS = [
 ("V1", [
  ("Hi everyone.", None),
  ("I built a system that takes a video idea, plans and generates the shots, reviews the results, and turns everything into a finished video.", None),
  ("For this demo, I'll quickly show you the process and the final output.", None)]),
 ("V2", [
  ("The process starts with a simple request.", None),
  ("Instead of giving Conductor a long prompt every time, I moved the recurring instructions into the workflow.", None),
  ("Now I can give it a short request, and the system handles the rest of the process.", None)]),
 ("V3", [
  ("The first thing the system does is look at this existing video library.", None),
  ("This library gives the system examples of different video styles, pacing, transitions, and storytelling.", None),
  ("It uses those references as inspiration to plan a new video, rather than copying one directly.", None)]),
 ("V4a", [
  ("After reviewing the references, the system breaks the idea into individual shots.", None),
  ("For this video, it created four shots with their own purpose, timing, copy, and visual direction.", None)]),
 ("V4b", [
  ("Here, I'm showing three of them: the initial brief, the campaign idea, and how that idea expands into different marketing assets.", None),
  ("For this project, the system chose HyperFrames because the video needed precise text, UI, and layout instead of generative footage.",
   # plain "UI" is read as one smooth "you-eye"; the earlier "U.I." hint split the letters
   "For this project, the system chose Hyper Frames because the video needed precise text, UI, and layout instead of generative footage.")]),
 ("V4c", [
  ("For other videos, it can use models available through Fal when the shot needs things like cinematic movement or generated footage.", None),
  ("The idea is to choose the method that best fits the shot, instead of using the same model for everything.", None)]),
 ("V5", [
  ("Once the individual shots are ready, they're combined into the final video.", None),
  ("The workflow then checks things like timing, transitions, audio, and the final output before considering the video complete.", None)]),
 ("V6", [
  ("For every finished video, the system creates its own reverse-engineering document.", "For every finished video, the system creates its own reverse engineering document."),
  ("This records how the video was made, including the prompts, structure, methods used, revisions, and key learnings.", None),
  ("The workflow also checks that this file exists before the video can be marked complete.", None)]),
 ("V7", [
  ("And this is the final video produced through that workflow.", None)]),
 ("V8", [
  ("The next phase I'm working on is human realism, especially improving natural movement, hands, eye direction, and longer scenes with people.", None),
  ("I'm keeping that research separate for now while I continue testing and improving it.", None)]),
]
