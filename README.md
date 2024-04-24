# Rules of NotesHub
1) DO NOT rename old files.
    - Renaming old files will break links to those files.
    - It is OK to rename new files, but as soon as a file is referenced by another file do not rename it.
2) AVOID editing files that other people are editing.
    - This will help prevent merge conflicts.
    - Merge errors can be resolved. But it is better to avoid them. They may lead to some data loss.
3) When possible, link to other files.
    - The goal of this note taking method is to create a network of files.
    - This helps to reduce redundancy and conflicts in our notes and research.
4) Use [MarkDown](https://www.markdownguide.org/tools/noteshub/) formatting as much as possible. When editing a file press the ⓘ button to see a list of all markdown formatting options available.

# File Creation best practices
- Use underscores (_) instead of spaces.
- Don't be too specific with names.
  - If it can be a section in a different file, make it a section in that file.

Good | Bad
-|-
KWO_Measurements | KWO_overnight_measurements_3-16-2024
MXene_Cancer_Detection_Mechanisms | MXene_Cancer_Detection_Mechanism_Possibility_4
CrWO_Synthesis | CrWO_Failed_Test_Batches
Noise_In_Measurements | The_Stupid_Keithley_Is_Acting_Up_Again

- If a section in a file gets too large, break it off into a new file. Link to the new file in place of the old file.
  - **Example:** File "A" has a section called "B". Section B is extremely large.
    - Create a new file called "B".
    - move contents from file A section B into file B.
    - Remove contents from file A section B.
    - Create link to file B in file A section B.

# Merge conflict
If multiple people are editing a note, a merge conflicts can occur.

If during the notebook synchronization notes can't be merged without conflicts, two alternative variants will be provided so you can pick the right one.

```
:::conflict{variant=a}
some text
:::

:::conflict{variant=d}
altered text
:::
```

:::conflict{variant=a}
some text
:::

:::conflict{variant=d}
altered text
:::

