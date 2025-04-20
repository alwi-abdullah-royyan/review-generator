# Review Generator Script

This script helps you generate structured game reviews with a sleek BBCode styling. You can easily create a structured review in a text editor, and the script will process your input into a nicely formatted BBCode or plain text review. Additionally, it can integrate AI-powered enhancements for your content using Groq's API.

---

## Requirements

### Libraries:
- **pyperclip**: For clipboard manipulation (copying the generated BBCode).
- **groq**: For AI-powered enhancements (using Groq's LLaMA model).

### AI Script Requirement:
This script uses a **Groq API token** to run LLaMA via Groq's backend. To enable AI functionality:
1. Visit [Groq's Console](https://console.groq.com/) and generate your API token.
2. Save the token in a file named `token.txt` in the same directory as the script.

---

## How to Use

### 1. **Install Python & Dependencies**

Before running the script, ensure you have **Python** installed. You can install the required libraries by running the following:

```bash
python install_requirement.py
```

### 2. **Run the Script**

- For **Windows**: Run `make_review_windows.py`
- For **Linux**: Run `make_review_linux.py`
- Or just run `review_generator.py` for platform-agnostic usage.

### 3. **Text Editor Opens**

Once you run the script, it will open a text editor where you can start writing your review. Sections of your review are indicated by `###`. Common sections include:
- `### game` - Game title and information
- `### main` - Main review content
- `### gameplay` - Gameplay mechanics
- `### combat` - Combat system
- `### art` - Art and visuals
- `### story` - Storyline and narrative
- `### pros` - Positive points
- `### cons` - Negative points
- `### tldr` - TL;DR summary

#### Tip:
- If you leave a section blank (e.g., `### gameplay`), it will be ignored in the final review.
- Once you're done, save and close the text editor.

### 4. **Processing the Review**

The script will process the review text you’ve written and structure it accordingly. It will automatically:
- Generate a **BBCode** version of your review, which will be copied to your clipboard by default.
- Save the **BBCode** version in `compiled_review_bbcode.txt`.
- Save the **regular** version (plain text) in `compiled_review.txt`.

### 5. **(Optional) Enhance with AI**

If you want to enhance your review with AI-generated content, follow these steps:

1. Ensure you have a **Groq API token** stored in `token.txt`.
2. After you finish writing your review and close the editor, the script will ask if you want to enhance each section using AI.
   - Type **`yes`** to use AI to enhance that section.
   - Type **`no`** to keep your original content.
   - Type **`skip`** to skip that section entirely.
   - If a section is blank, the script will automatically skip it.

The AI feature uses **Groq's LLaMA model** to enhance various parts of your review, such as the introduction, gameplay description, combat mechanics, story, etc.

---

## Example Output

- The **BBCode version** of the review will be copied to your clipboard and saved in `compiled_review_bbcode.txt`.
- The **regular text** version (without BBCode) will be saved in `compiled_review.txt`.

Both files will be available for you to share or edit further.

---

## Contributing

Feel free to fork this repository, contribute code, or suggest improvements via issues and pull requests.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
