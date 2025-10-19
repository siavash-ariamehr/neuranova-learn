import os
from typing import List, Dict, Optional
import httpx
from openai import AsyncOpenAI

class LessonGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        self.oer_commons_url = "https://www.oercommons.org/api/v1/resources"
    
    async def generate_with_gpt4o(
        self,
        subject: str,
        difficulty: str,
        age_range: str,
        language: str = "en"
    ) -> Dict:
        prompt = f"""Create an engaging interactive STEM lesson for {subject} at {difficulty} level for {age_range} students.
        
Include:
- Clear learning objectives
- Interactive elements and hands-on activities
- Real-world applications
- Assessment questions
- AR/VR simulation ideas if applicable

Format the response as JSON with keys: title, content, interactive_elements, ar_vr_content, assessment_questions"""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert STEM educator creating engaging lessons."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            lesson_data = response.choices[0].message.content
            return {
                "title": f"{subject} Lesson - {difficulty}",
                "content": lesson_data,
                "subject": subject,
                "difficulty": difficulty,
                "age_range": age_range,
                "language": language,
                "source": "GPT-4o Generated"
            }
        except Exception as e:
            return {
                "title": f"Error generating lesson",
                "content": str(e),
                "subject": subject,
                "difficulty": difficulty,
                "age_range": age_range,
                "language": language,
                "source": "Error"
            }
    
    async def import_from_oer_commons(
        self,
        subject: str,
        limit: int = 10
    ) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.oer_commons_url,
                    params={
                        "f.search": subject,
                        "f.sublevel": "higher-education",
                        "limit": limit
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    lessons = []
                    
                    for resource in data.get("results", []):
                        lessons.append({
                            "title": resource.get("title", ""),
                            "content": resource.get("description", ""),
                            "subject": subject,
                            "difficulty": "intermediate",
                            "age_range": "high_school",
                            "language": "en",
                            "source": f"OER Commons - {resource.get('id', '')}"
                        })
                    
                    return lessons
        except Exception:
            pass
        
        return []

lesson_generator = LessonGenerator()
