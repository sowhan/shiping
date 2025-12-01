import React from 'react';
import {
  Book, Search, MessageCircle, FileText, Video, ExternalLink,
  ChevronRight, HelpCircle, Mail, Phone
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent, Input, Button } from '../components/ui';

interface HelpTopic {
  id: string;
  title: string;
  description: string;
  articles: number;
  icon: React.ReactNode;
}

interface FAQ {
  question: string;
  answer: string;
}

/**
 * Help page with documentation and support resources.
 */
export const Help: React.FC = () => {
  const helpTopics: HelpTopic[] = [
    {
      id: 'getting-started',
      title: 'Getting Started',
      description: 'Learn the basics of maritime route planning',
      articles: 12,
      icon: <Book className="w-6 h-6 text-blue-600" />
    },
    {
      id: 'route-planning',
      title: 'Route Planning',
      description: 'Create and optimize shipping routes',
      articles: 18,
      icon: <FileText className="w-6 h-6 text-green-600" />
    },
    {
      id: 'vessel-management',
      title: 'Vessel Management',
      description: 'Track and manage your fleet',
      articles: 8,
      icon: <Video className="w-6 h-6 text-purple-600" />
    },
    {
      id: 'api-documentation',
      title: 'API Documentation',
      description: 'Integrate with our REST API',
      articles: 24,
      icon: <FileText className="w-6 h-6 text-orange-600" />
    }
  ];

  const faqs: FAQ[] = [
    {
      question: 'How do I calculate an optimal route?',
      answer: 'Go to the Dashboard, enter your origin and destination ports, select your vessel type and optimization criteria, then click "Calculate Routes". The system will analyze multiple factors including distance, weather, and port congestion to provide optimal route options.'
    },
    {
      question: 'What optimization criteria can I choose?',
      answer: 'You can optimize routes for: Fastest (minimum travel time), Most Economical (lowest total cost), Most Reliable (highest schedule reliability), or Balanced (optimal trade-off between all factors).'
    },
    {
      question: 'How accurate are the ETA predictions?',
      answer: 'Our ETA predictions achieve >98% accuracy by incorporating real-time weather data, port congestion information, vessel specifications, and historical voyage data. ETAs are continuously updated as conditions change.'
    },
    {
      question: 'Can I track vessels in real-time?',
      answer: 'Yes, the Vessel Tracking feature provides real-time position updates via AIS data integration. You can view vessel status, speed, course, and estimated arrival times for any tracked vessel.'
    },
    {
      question: 'What ports are available in the database?',
      answer: 'Our database includes over 50,000 ports worldwide with detailed information including coordinates, facilities, operational status, and vessel size restrictions. Port data is continuously updated from authoritative maritime sources.'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto">
        <div className="w-16 h-16 bg-maritime-blue/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <HelpCircle className="w-8 h-8 text-maritime-blue" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900">How can we help you?</h1>
        <p className="text-gray-500 mt-2">
          Search our documentation or browse help topics below
        </p>
        <div className="mt-6 relative max-w-lg mx-auto">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            type="search"
            placeholder="Search for help..."
            className="pl-10"
          />
        </div>
      </div>

      {/* Help Topics */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        {helpTopics.map((topic) => (
          <Card key={topic.id} className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="pt-6">
              <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                {topic.icon}
              </div>
              <h3 className="font-semibold text-gray-900 mb-1">{topic.title}</h3>
              <p className="text-sm text-gray-500 mb-3">{topic.description}</p>
              <Link
                to={`/docs/${topic.id}`}
                className="text-sm text-maritime-blue hover:underline flex items-center gap-1"
              >
                {topic.articles} articles
                <ChevronRight className="w-4 h-4" />
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* FAQs */}
      <Card>
        <CardHeader>
          <CardTitle>Frequently Asked Questions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="divide-y divide-gray-100">
            {faqs.map((faq, index) => (
              <details key={index} className="group py-4">
                <summary className="flex items-center justify-between cursor-pointer list-none">
                  <span className="font-medium text-gray-900">{faq.question}</span>
                  <ChevronRight className="w-5 h-5 text-gray-400 group-open:rotate-90 transition-transform" />
                </summary>
                <p className="mt-3 text-gray-600 text-sm leading-relaxed pl-0">
                  {faq.answer}
                </p>
              </details>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Contact Support */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="bg-gradient-to-br from-maritime-blue to-maritime-blue/80 text-white">
          <CardContent className="pt-6">
            <MessageCircle className="w-10 h-10 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Contact Support</h3>
            <p className="text-white/80 text-sm mb-4">
              Our support team is available 24/7 to help with any questions.
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4" />
                <span>support@maritime-routes.com</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4" />
                <span>+1 (555) 123-4567</span>
              </div>
            </div>
            <Button variant="outline" className="mt-4 bg-white/10 border-white/20 hover:bg-white/20">
              Start Chat
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <Book className="w-10 h-10 text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Documentation</h3>
            <p className="text-gray-500 text-sm mb-4">
              Comprehensive guides and API documentation for developers.
            </p>
            <div className="space-y-2">
              <Link
                to="/docs/api"
                className="flex items-center gap-2 text-sm text-gray-700 hover:text-maritime-blue"
              >
                <FileText className="w-4 h-4" />
                API Reference
                <ExternalLink className="w-3 h-3 ml-auto" />
              </Link>
              <Link
                to="/docs/guides"
                className="flex items-center gap-2 text-sm text-gray-700 hover:text-maritime-blue"
              >
                <Book className="w-4 h-4" />
                User Guides
                <ExternalLink className="w-3 h-3 ml-auto" />
              </Link>
              <Link
                to="/docs/tutorials"
                className="flex items-center gap-2 text-sm text-gray-700 hover:text-maritime-blue"
              >
                <Video className="w-4 h-4" />
                Video Tutorials
                <ExternalLink className="w-3 h-3 ml-auto" />
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Help;
