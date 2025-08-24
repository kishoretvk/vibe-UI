import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const TestShadcn: React.FC = () => {
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">shadcn/ui Component Test</h1>
      
      {/* Button Test */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Buttons</h2>
        <div className="flex space-x-2">
          <Button>Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="link">Link</Button>
        </div>
      </div>
      
      {/* Card Test */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Cards</h2>
        <Card className="w-[350px]">
          <CardHeader>
            <CardTitle>Card Title</CardTitle>
            <CardDescription>Card Description</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Card Content</p>
          </CardContent>
          <CardFooter>
            <Button>Card Footer</Button>
          </CardFooter>
        </Card>
      </div>
      
      {/* Badge Test */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Badges</h2>
        <div className="flex space-x-2">
          <Badge>Default</Badge>
          <Badge variant="secondary">Secondary</Badge>
          <Badge variant="destructive">Destructive</Badge>
          <Badge variant="outline">Outline</Badge>
        </div>
      </div>
      
      {/* Alert Test */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Alerts</h2>
        <Alert>
          <AlertTitle>Heads up!</AlertTitle>
          <AlertDescription>
            This is a default alert component.
          </AlertDescription>
        </Alert>
        
        <Alert variant="destructive" className="mt-2">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>
            This is a destructive alert component.
          </AlertDescription>
        </Alert>
      </div>
    </div>
  );
};

export default TestShadcn;