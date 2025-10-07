import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useLanguage } from '@/contexts/LanguageContext';

interface Lesson {
  id: number;
  title: string;
  subject: string;
  difficulty: string;
  language: string;
}

interface UserProgress {
  total_lessons_started: number;
  completed_lessons: number;
  average_score: number;
  dropout_risk_percentage: number;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { currentLanguage, setLanguage, supportedLanguages, translateText } = useLanguage();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [translatedLessons, setTranslatedLessons] = useState<{ [key: number]: string }>({});
  const [progress] = useState<UserProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [translating, setTranslating] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    if (currentLanguage !== 'en' && lessons.length > 0) {
      translateLessonTitles();
    } else {
      setTranslatedLessons({});
    }
  }, [currentLanguage, lessons]);

  const translateLessonTitles = async () => {
    setTranslating(true);
    const translations: { [key: number]: string } = {};
    
    for (const lesson of lessons) {
      try {
        const translated = await translateText(lesson.title);
        translations[lesson.id] = translated;
      } catch (error) {
        console.error(`Failed to translate lesson ${lesson.id}:`, error);
        translations[lesson.id] = lesson.title;
      }
    }
    
    setTranslatedLessons(translations);
    setTranslating(false);
  };

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      const lessonsResponse = await fetch('http://localhost:8000/api/lessons', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const lessonsData = await lessonsResponse.json();
      setLessons(lessonsData);

      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-4xl font-bold">NeuraNova Learn</h1>
        <div className="flex items-center gap-4">
          <Select value={currentLanguage} onValueChange={setLanguage}>
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Select Language" />
            </SelectTrigger>
            <SelectContent>
              {supportedLanguages.map((lang) => (
                <SelectItem key={lang.code} value={lang.code}>
                  {lang.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Badge variant="outline">Student Dashboard</Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Lessons Started</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{progress?.total_lessons_started || 0}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Completed</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{progress?.completed_lessons || 0}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Average Score</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{progress?.average_score || 0}%</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Available Lessons</CardTitle>
          <CardDescription>
            Explore interactive STEM lessons with AR/VR simulations
            {translating && currentLanguage !== 'en' && (
              <span className="ml-2 text-sm text-blue-600">Translating to {supportedLanguages.find(l => l.code === currentLanguage)?.name}...</span>
            )}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {lessons.map((lesson) => (
              <Card key={lesson.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="text-lg">
                    {translatedLessons[lesson.id] || lesson.title}
                  </CardTitle>
                  <div className="flex gap-2">
                    <Badge>{lesson.subject}</Badge>
                    <Badge variant="outline">{lesson.difficulty}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <Button 
                    className="w-full"
                    onClick={() => navigate('/ar-lesson', { state: { lesson } })}
                  >
                    Start Lesson
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {progress && progress.dropout_risk_percentage > 50 && (
        <Card className="border-red-500">
          <CardHeader>
            <CardTitle className="text-red-600">Learning Support</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Our AI has detected you might need additional support. Consider:</p>
            <ul className="list-disc list-inside mt-2">
              <li>Reviewing previous lessons</li>
              <li>Joining a study group</li>
              <li>Contacting your teacher</li>
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
