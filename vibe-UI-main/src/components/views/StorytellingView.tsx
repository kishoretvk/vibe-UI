import React, { useState, useEffect } from 'react';
import { useDataContext } from '../../contexts/DataContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const StorytellingView: React.FC = () => {
  const { data, loading, error } = useDataContext();
  const [story, setStory] = useState<any>(null);
  const [storyLoading, setStoryLoading] = useState(false);
  const [storyError, setStoryError] = useState<string | null>(null);

  useEffect(() => {
    if (data && data.length > 0) {
      generateStory();
    }
  }, [data]);

  const generateStory = async () => {
    setStoryLoading(true);
    setStoryError(null);
    
    try {
      // Call the AI analysis service
      const response = await fetch('/api/ai/storytelling', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const storyData = await response.json();
      setStory(storyData);
    } catch (err) {
      setStoryError('Failed to generate story. Please try again.');
      console.error('Story generation error:', err);
    } finally {
      setStoryLoading(false);
    }
  };

  if (loading) {
    return <div className="p-4">Loading data...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  if (!data || data.length === 0) {
    return <div className="p-4">No data available for analysis.</div>;
  }

  return (
    <div className="p-4 space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">AI-Powered Data Storytelling</h2>
        <Button 
          onClick={generateStory}
          disabled={storyLoading}
        >
          {storyLoading ? 'Generating...' : 'Regenerate Story'}
        </Button>
      </div>

      {storyLoading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      )}

      {storyError && (
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>
            {storyError}
          </AlertDescription>
        </Alert>
      )}

      {story && !storyLoading && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{story.title}</CardTitle>
              <CardDescription>{story.summary}</CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Key Insights</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {story.insights.map((insight: any, index: number) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                    <div className="flex justify-between items-center">
                      <span className="font-medium">{insight.type.charAt(0).toUpperCase() + insight.type.slice(1)}</span>
                      <div className="flex items-center space-x-2">
                        <Badge variant="secondary">Confidence: {(insight.confidence * 100).toFixed(0)}%</Badge>
                      </div>
                    </div>
                    <p className="mt-1">{insight.description}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5 space-y-2">
                {story.recommendations.map((recommendation: string, index: number) => (
                  <li key={index} className="text-gray-700 dark:text-gray-300">{recommendation}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default StorytellingView;