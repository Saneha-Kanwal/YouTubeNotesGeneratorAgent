"""
OpenAI client wrapper using Agent SDK syntax.
Provides functions for Whisper transcription, GPT note generation, and translation.
"""
import os
from openai import OpenAI
from pathlib import Path


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio file using OpenAI Whisper API.
    Handles large files by automatically chunking and combining transcripts.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        str: Combined transcript text from all chunks
    """
    import os
    from app.audio_chunker import split_audio_into_chunks
    
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB OpenAI limit
    
    try:
        # Check file size before uploading
        file_size = os.path.getsize(audio_path)
        
        # If file is small enough, transcribe directly
        if file_size <= MAX_FILE_SIZE:
            with open(audio_path, "rb") as audio_file:
                file_name = os.path.basename(audio_path)
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=(file_name, audio_file, "audio/mpeg"),
                    response_format="text",
                )
            return transcript
        
        # File is too large - split into chunks and transcribe each
        print(f"📦 Audio file ({file_size / 1024 / 1024:.2f}MB) exceeds 25MB limit. Splitting into chunks...")
        
        chunks = split_audio_into_chunks(audio_path, max_chunk_size_mb=20.0)
        transcripts = []
        
        print(f"🔄 Transcribing {len(chunks)} chunks...")
        
        for i, chunk_path in enumerate(chunks):
            chunk_size = os.path.getsize(chunk_path) / (1024 * 1024)
            print(f"📝 Transcribing chunk {i+1}/{len(chunks)} ({chunk_size:.2f}MB)...")
            
            try:
                with open(chunk_path, "rb") as chunk_file:
                    file_name = os.path.basename(chunk_path)
                    chunk_transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=(file_name, chunk_file, "audio/mpeg"),
                        response_format="text",
                    )
                transcripts.append(chunk_transcript)
                print(f"✅ Chunk {i+1}/{len(chunks)} transcribed successfully")
            except Exception as e:
                print(f"⚠️ Error transcribing chunk {i+1}: {e}")
                # Continue with other chunks even if one fails
                continue
            
            # Clean up chunk file
            try:
                os.remove(chunk_path)
            except:
                pass
        
        if not transcripts:
            raise Exception("Failed to transcribe any audio chunks")
        
        # Combine all transcripts
        combined_transcript = "\n\n".join(transcripts)
        print(f"✅ Successfully transcribed and combined {len(transcripts)} chunks")
        
        return combined_transcript
        
    except Exception as e:
        error_msg = str(e)
        # Provide more helpful error messages
        if "413" in error_msg or "Maximum content size" in error_msg:
            raise Exception(
                f"Audio file too large for transcription even after chunking. "
                f"Please try a shorter video or contact support."
            )
        raise Exception(f"Transcription failed: {error_msg}")


async def generate_notes(transcript: str) -> str:
    """
    Generate structured notes from transcript using GPT with Agent SDK syntax.
    
    The notes must include:
    - Main heading
    - Subheadings
    - Bullet points
    - Key insights
    - Important quotes
    - Final summary
    - Actionable takeaways
    """
    system_prompt = """You are a highly skilled note-taking assistant. When given a transcript of a YouTube video, produce cleanly structured study notes. Requirements:

- Output in Markdown.
- Provide a top-level title extracted from the video.
- Provide a one-sentence TL;DR summary.
- Organize content into major headings (H2), subheadings (H3), and bullet lists.
- Highlight key insights in a section titled "Key Insights" with numbered bullets.
- Include a section "Important Quotes" containing verbatim short quotes from the transcript flagged by timestamps (if timestamps exist).
- End with "Actionable Takeaways" — 5 practical actions the reader can take.
- Keep each bullet concise (6–18 words).
- If transcript contains code blocks, format them in fenced code blocks.
- Always keep the original transcript paragraphs as reference in a collapsed details block called "Full Transcript".

Return only the Markdown output."""

    user_prompt = f"Here is the transcript:\n\n{transcript}\n\nReturn only the Markdown output."

    try:
        # Use chat completion API (constitution allows this for note generation)
        response = client.chat.completions.create(
            model="gpt-4o",  # Using latest model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content or ""
    except Exception as e:
        raise Exception(f"Note generation failed: {str(e)}")


async def translate_text(text: str, target_language: str) -> str:
    """
    Translate text to target language while preserving Markdown structure.
    
    Uses OpenAI Agent SDK syntax to translate notes while keeping:
    - Headings structure
    - Code blocks unchanged
    - Markdown formatting intact
    """
    system_prompt = f"""You are a professional translator. Your task is to translate the following Markdown notes into the language with code '{target_language}'.

CRITICAL REQUIREMENTS:
1. Preserve ALL Markdown structure exactly (headings, lists, code blocks, links, etc.)
2. Do NOT translate code blocks, code snippets, or technical terms that should remain in English
3. Keep all heading levels (# ## ###) exactly as they are
4. Preserve all formatting symbols (**, _, `, etc.)
5. Translate only the actual text content, not the structure
6. Maintain the same tone and style as the original
7. If a section is already in the target language, leave it unchanged

Return the translated Markdown with the exact same structure."""

    user_prompt = f"Translate the following notes to language code '{target_language}':\n\n{text}"

    try:
        # Use chat completion API for translation
        response = client.chat.completions.create(
            model="gpt-4o",  # Using latest model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content or ""
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

