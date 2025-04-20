import ctypes
import win32clipboard
import os
import subprocess
import platform
import pyperclip
from groq import Groq
#ai functions
# Prompt for AI usage and validate Groq token
def check_ai_usage():
    print("This script uses a Groq API token runs on the LLaMA via Groq's backend. Visit https://console.groq.com/ to generate your token, and paste it into 'token.txt'.")
    print("Note: Avoid using explicit or overly suggestive language. The model may refuse to respond to such content.")
    print("this will not tries to enhance pros and cons part.")
    use_ai = input("Do you want to use AI? (yes/no): ").strip().lower()
    if use_ai == "yes":
        if not os.path.exists("token.txt"):
            print("❌ Error: token.txt not found.")
            return None

        with open("token.txt", "r", encoding="utf-8") as f:
            token = f.read().strip()

        if not token:
            print("❌ Error: Token is blank. Feature disabled.")
            return None

        try:
            client = Groq(api_key=token)
            client.models.list()  # Basic test call to validate token
            print("✅ Token valid. AI feature enabled.")
            return token
        except Exception as e:
            print(f"❌ Error validating token: {e}")
            return None
    else:
        print("AI feature disabled.")
        return None


# Use Groq to call LLaMA 3 and generate text
def call_ai_to_generate_content(prompt, api_key):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for writing game reviews."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error calling AI: {e}")
        return None


# Ask user if they want AI enhancement per section
def process_with_ai(sections, api_key):

    prompts = {
        "main": f"Enhance the introduction of the game review. Add more details, but do not add introductory phrases or rewrite the whole section. Only expand on the existing text: {sections.get('main', '')}",
        "gameplay": f"Enhance the description of the gameplay mechanics. Add more details, but do not add introductory phrases or rewrite the whole section. Only expand on the existing text: {sections.get('gameplay', '')}",
        "combat": f"Add more detail to the combat system description, without writing a full section. Avoid any introductory sentences like 'Let’s dive into combat.' Only enhance the current description: {sections.get('combat', '')}",
        "art": f"Expand on the description of the game's art style, without any introduction. Simply add more relevant detail to the existing description: {sections.get('art', '')}",
        "story": f"Enhance the description of the game’s story without adding any introductory text like 'Here’s the story breakdown'. Focus solely on improving the original description: {sections.get('story', '')}",
        "tldr": f"Write a concise TL;DR summary. Avoid any introductory sentences and just summarize the review: {sections.get('tldr', '')}"
    }


    for key, prompt in prompts.items():
        section_content = sections.get(key, "").strip()  # Strip any leading/trailing spaces
        if section_content:  # Only proceed if the section is not blank
            print(f"\n--- Original '{key}' Section ---\n{section_content}")
            use_ai = input(f"\nDo you want to use AI to enhance the '{key}' section? (yes/no/skip): ").strip().lower()
            if use_ai == "yes":
                print(f"Using AI to process the '{key}' section...")
                ai_result = call_ai_to_generate_content(prompt, api_key)
                if ai_result:
                    print(f"\n--- AI-Generated '{key}' Section ---\n{ai_result}")
                    choice = input("Use the AI-generated version? (yes/no): ").strip().lower()
                    if choice == "yes":
                        sections[key] = ai_result
                        print(f"✅ AI version accepted for '{key}'.")
                    else:
                        print(f"🛑 Kept original for '{key}'.")
                else:
                    print(f"❌ AI failed to process the '{key}' section.")
            elif use_ai == "skip":
                print(f"Skipping AI entire section.")
                return
            else:
                print(f"Skipping AI for the '{key}' section.")
        else:
            print(f"Skipping '{key}' section as it's empty.")



#end of ai functions

def delete_old_files():
    for fname in ["compiled_review_bbcode.txt", "compiled_review.txt"]:
        if os.path.exists(fname):
            os.remove(fname)

def generate_default_review():
    with open("review.txt", "w", encoding="utf-8") as f:
        f.write("""You can close this after you're done writing. Don't forget to save it!

Instructions:
- You can leave any section blank if you don't wish to include it in the review.
- If a section is left blank, it will not be included in the final review when generated.

### game
title

### main
review

### gameplay
Gameplay review

### combat
combat

### art
art

### story
story

### pros
pros

### cons
cons

### tldr
tldr.
""")


def ensure_review_exists():
    if not os.path.exists("review.txt"):
        print("review.txt not found. Creating one...")
        generate_default_review()
        print("New review.txt generated.\n")

def open_editor_and_wait(filename):
    system = platform.system()

    if system == "Windows":
        print("Opening review.txt in Notepad. Close it when you're ready.")
        subprocess.run(["notepad", filename])
    elif system == "Linux":
        # This assumes `gedit` is installed on the Linux system, or you could replace it with `nano`, `vim`, etc.
        print("Opening review.txt in gedit. Close it when you're ready.")
        subprocess.run(["gedit", filename])
    elif system == "Darwin":  # For macOS
        print("Opening review.txt in TextEdit. Close it when you're ready.")
        subprocess.run(["open", "-a", "TextEdit", filename])
    else:
        print("Unsupported OS. Please edit the file manually and run this again.")

def open_output_in_editor():
    subprocess.Popen(["notepad", "compiled_review.txt"])
    
def build_bbcode_clipboard_fragment(bbcode_fragment):
    bbcode = f"{bbcode_fragment}"
    return bbcode.encode("utf-16le")

def copy_bbcode_to_clipboard(bbcode_fragment):
    # Assuming the fragment is properly encoded in UTF-16LE (if you really need that)
    bbcode_clipboard = build_bbcode_clipboard_fragment(bbcode_fragment)
    
    # Ensure the text is in a format pyperclip can handle (plain string, not raw bytes)
    # We need to decode it to a Python string if it's in UTF-16LE
    if isinstance(bbcode_clipboard, bytes):
        bbcode_clipboard = bbcode_clipboard.decode('utf-16le')

    # Now copy it to the clipboard
    pyperclip.copy(bbcode_clipboard)


def parse_sections(filename):
    sections = {}
    current_section = None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("### "):
                current_section = line[4:].strip().lower()
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line)
    return {
        key: '\n'.join(value).strip() if key in ['main','gameplay','combat','art','story', 'tldr', 'game'] 
        else [line.strip() for line in value if line.strip()]
        for key, value in sections.items()
    }

def generate_review_bbcode(sections):
    game_info = sections.get("game", "Unknown Game")
    yapping = sections.get("main", "")
    gameplay = sections.get("gameplay", "")
    combat = sections.get("combat", "")
    art = sections.get("art", "")
    story = sections.get("story", "")
    pros = sections.get("pros", [])
    cons = sections.get("cons", [])
    tldr = sections.get("tldr", "")

    # BBCode formatting for the title
    title_bbcode = f'[B][SIZE=6]{game_info}[/SIZE][/B]\n\n'

    # Main body with newline after each line, check if content exists
    body_bbcode = '\n'.join([f'{line}' for line in yapping.split('\n') if line.strip()])
    if body_bbcode:  # Only add newline if body has content
        body_bbcode += '\n\n'
    
    body1_bbcode = '\n'.join([f'{line}' for line in gameplay.split('\n') if line.strip()])
    if body1_bbcode:  
        body1_bbcode += '\n\n'
    
    body2_bbcode = '\n'.join([f'{line}' for line in combat.split('\n') if line.strip()])
    if body2_bbcode: 
        body2_bbcode += '\n\n'
    
    body3_bbcode = '\n'.join([f'{line}' for line in art.split('\n') if line.strip()])
    if body3_bbcode:  
        body3_bbcode += '\n\n'
    
    body4_bbcode = '\n'.join([f'{line}' for line in story.split('\n') if line.strip()])
    if body4_bbcode:  
        body4_bbcode += '\n\n'

    pros_bbcode = ''
    if pros:  
        pros_bbcode = '[COLOR=rgb(0, 128, 0)][B]Pros[/B][/COLOR]\n'
        pros_bbcode += '\n'.join([f'[COLOR=rgb(0, 128, 0)] +[/COLOR] {p}' for p in pros]) + '\n\n'

    cons_bbcode = ''
    if cons:  
        cons_bbcode = '[COLOR=rgb(184, 49, 47)][B]Cons[/B][/COLOR]\n'
        cons_bbcode += '\n'.join([f'[COLOR=rgb(184, 49, 47)] -[/COLOR] {c}' for c in cons]) + '\n\n'

    tldr_bbcode = ''
    if tldr.strip():  
        tldr_bbcode = '[B][COLOR=rgb(255, 165, 0)]TL;DR:[/COLOR][/B] ' 
        tldr_bbcode += f'{tldr}\n'

    # Combine everything with appropriate line breaks between sections
    return title_bbcode + body_bbcode + body1_bbcode + body2_bbcode + body3_bbcode + body4_bbcode + pros_bbcode + cons_bbcode + tldr_bbcode

    
def generate_review(sections):
    game_info = sections.get("game", "Unknown Game")
    yapping = sections.get("main", "")
    gameplay = sections.get("gameplay", "")
    combat = sections.get("combat", "")
    art = sections.get("art", "")
    story = sections.get("story", "")
    pros = sections.get("pros", [])
    cons = sections.get("cons", [])
    tldr = sections.get("tldr", "")

    pros_text = '\n'.join([f'+{p}' for p in pros]) if pros else ""
    cons_text = '\n'.join([f'-{c}' for c in cons]) if cons else ""

    # Start building the review string
    review = f"[{game_info}]\n"

    # Only add sections if they contain content
    if yapping.strip():
        review += f"{yapping}\n\n"
    
    if gameplay.strip():
        review += f"{gameplay}\n\n"
    
    if combat.strip():
        review += f"{combat}\n\n"
    
    if art.strip():
        review += f"{art}\n\n"
    
    if story.strip():
        review += f"{story}\n\n"
    
    if pros_text:
        review += f"Pros\n{pros_text}\n\n"
    
    if cons_text:
        review += f"Cons\n{cons_text}\n\n"
        
    if tldr.strip():
        review += f"Tl;Dr\n{tldr}"

    return review.strip()  # Remove any trailing spaces/newlines


    
if __name__ == "__main__":
    delete_old_files()
    ensure_review_exists()
    api_key = check_ai_usage()
    open_editor_and_wait("review.txt")

    try:
        sections = parse_sections("review.txt")
        if api_key:
            print("AI feature is enabled.")
            process_with_ai(sections, api_key)  # Process the review sections with AI if api_key exists
        else:
            print("AI feature is not enabled. Proceeding without AI.")

        compiled_bbcode = generate_review_bbcode(sections)
        compiled_text = generate_review(sections)

        with open("compiled_review_bbcode.txt", "w", encoding="utf-8") as out:
            out.write(compiled_bbcode)
        with open("compiled_review.txt", "w", encoding="utf-8") as out:
            out.write(compiled_text)

        copy_bbcode_to_clipboard(compiled_bbcode)
        print("\n✅ Styled review copied to clipboard (BBCode)!")
        open_output_in_editor()

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("Something went wrong during execution.")
        print("Read the error above. If you're not sure what went wrong, press Enter to reset the review.txt to its default format.")
        choice = input("Press [Enter] to reset review.txt, or [Ctrl+C] to cancel: ")
        print("Restoring review to default state...")
        generate_default_review()
