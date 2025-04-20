import ctypes
import win32clipboard
import os
import subprocess
import platform
import pyperclip

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
    open_editor_and_wait("review.txt")

    try:
        sections = parse_sections("review.txt")
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
