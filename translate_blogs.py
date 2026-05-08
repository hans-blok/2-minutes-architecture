import os
from deep_translator import GoogleTranslator

def translate_markdown(filepath, outpath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    translator = GoogleTranslator(source='nl', target='en')
    
    # Split by double newline to preserve paragraph structure and respect the 5000 character limit
    chunks = content.split('\n\n')
    translated_chunks = []
    
    for chunk in chunks:
        if chunk.strip():
            try:
                # Small sub-chunks if paragraph itself is too large
                if len(chunk) > 4999:
                    sub_chunks = [chunk[i:i+4900] for i in range(0, len(chunk), 4900)]
                    sub_translated = [translator.translate(sc) for sc in sub_chunks]
                    translated_chunks.append(''.join(sub_translated))
                else:
                    translated_chunks.append(translator.translate(chunk))
            except Exception as e:
                print(f"Failed to translate chunk in {filepath}: {e}")
                translated_chunks.append(chunk)  # Fallback to original text for this chunk
        else:
            translated_chunks.append('')
            
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_chunks))

def main():
    content_dir = os.path.join('content', 'nl')
    out_dir = os.path.join('content', 'en')
    os.makedirs(out_dir, exist_ok=True)
    
    for filename in os.listdir(content_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(content_dir, filename)
            outpath = os.path.join(out_dir, filename)
            print(f"Translating {filename}...")
            translate_markdown(filepath, outpath)
            print(f"Saved translation to {outpath}")

if __name__ == '__main__':
    main()
