import React, { useState } from 'react';
import { Brain, Send, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react';
import QuestionCard from './QuestionCard';
import ResultCard from './ResultCard';
import { questions } from './questions';
import { predictPersonality } from '../utils/aiPredictor';
import type { Question, PersonalityResult } from './types';

const WelcomeScreen = ({ onStart }: { onStart: (name: string) => void }) => {
  const [name, setName] = useState('');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black py-12">
      <div className="max-w-3xl mx-auto p-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-3 bg-white rounded-xl">
              <Brain className="w-8 h-8 text-black" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">
                AI-Powered Personality Insights
              </h1>
              <p className="text-gray-300">Discover your unique personality traits</p>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-white text-sm font-medium mb-2">
                What's your name?
              </label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
                placeholder="Enter your name"
              />
            </div>

            <button
              onClick={() => onStart(name.trim())}
              disabled={!name.trim()}
              className="w-full px-6 py-3 bg-white text-black rounded-xl hover:bg-gray-100 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <Send className="w-5 h-5" />
              Start Personality Test
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const calculateResults = async (answers: number[], userName: string): Promise<PersonalityResult> => {
  const aiPredictions = await predictPersonality(answers);
  
  const dominantTrait = Object.entries(aiPredictions).reduce((a, b) => 
    aiPredictions[a] > aiPredictions[b[0]] ? a : b[0]
  );

  const getDominantTraitDescription = (trait: string) => {
    switch(trait) {
      case 'openness':
        return `${userName}, you are primarily characterized by your openness to experience. This makes you naturally curious, creative, and appreciative of art and beauty.`;
      case 'conscientiousness':
        return `${userName}, your dominant trait is conscientiousness. This makes you organized, responsible, and focused on achieving your goals.`;
      case 'extraversion':
        return `${userName}, you are predominantly extraverted. This means you thrive on social interaction and tend to be energetic and outgoing.`;
      case 'agreeableness':
        return `${userName}, your personality is dominated by agreeableness. This makes you compassionate, cooperative, and focused on others' well-being.`;
      case 'neuroticism':
        return `${userName}, your dominant trait is emotional stability. This means you tend to be resilient, calm, and composed under pressure.`;
    }
  };

  return {
    summary: getDominantTraitDescription(dominantTrait),
    dominantTrait,
    userName,
    traits: {
      openness: {
        name: "Openness to Experience",
        description: "Your level of curiosity, creativity, and preference for novel experiences",
        score: aiPredictions.openness,
        details: "People high in openness tend to be creative, curious, and intellectually adventurous. They appreciate art, nature, and new ideas, often seeking out unique experiences and perspectives.",
        color: "bg-indigo-500"
      },
      conscientiousness: {
        name: "Conscientiousness",
        description: "Your approach to organization, responsibility, and goal-oriented behavior",
        score: aiPredictions.conscientiousness,
        details: "Highly conscientious individuals are organized, responsible, and detail-oriented. They excel at planning, maintaining order, and achieving goals through disciplined effort.",
        color: "bg-blue-500"
      },
      extraversion: {
        name: "Extraversion",
        description: "Your energy level in social situations and preference for social interaction",
        score: aiPredictions.extraversion,
        details: "Extraverted people gain energy from social interactions and external stimulation. They tend to be outgoing, enthusiastic, and action-oriented, often seeking excitement and social connections.",
        color: "bg-yellow-500"
      },
      agreeableness: {
        name: "Agreeableness",
        description: "Your tendency towards compassion, cooperation, and consideration of others",
        score: aiPredictions.agreeableness,
        details: "Agreeable individuals are compassionate, cooperative, and considerate of others' feelings. They value harmony and tend to be trustworthy, helpful, and willing to compromise.",
        color: "bg-green-500"
      },
      neuroticism: {
        name: "Emotional Stability",
        description: "Your typical way of responding to stress and emotional situations",
        score: aiPredictions.neuroticism,
        details: "People with high emotional stability tend to be calm, resilient, and even-tempered. They handle stress well and maintain composure in challenging situations.",
        color: "bg-purple-500"
      }
    }
  };
};

export default function PersonalityTest() {
  const [answers, setAnswers] = useState<number[]>(Array(questions.length).fill(-1));
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<PersonalityResult | null>(null);
  const [userName, setUserName] = useState<string>('');
  const [hasStarted, setHasStarted] = useState(false);

  const handleStart = (name: string) => {
    setUserName(name);
    setHasStarted(true);
  };

  const handleAnswer = (value: number) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {
    setIsAnalyzing(true);
    try {
      const results = await calculateResults(answers, userName);
      setResult(results);
    } catch (error) {
      console.error('Error calculating results:', error);
      // Handle error appropriately
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetTest = () => {
    setAnswers(Array(questions.length).fill(-1));
    setCurrentQuestion(0);
    setResult(null);
    setHasStarted(false);
    setUserName('');
  };

  if (!hasStarted) {
    return <WelcomeScreen onStart={handleStart} />;
  }

  if (result) {
    return <ResultCard result={result} onReset={resetTest} />;
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100;
  const currentTrait = questions[currentQuestion].trait;
  const traitColors = {
    openness: "from-indigo-600 to-indigo-900",
    conscientiousness: "from-blue-600 to-blue-900",
    extraversion: "from-yellow-600 to-yellow-900",
    agreeableness: "from-green-600 to-green-900",
    neuroticism: "from-purple-600 to-purple-900"
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br ${traitColors[currentTrait]} transition-all duration-500`}>
      <div className="max-w-3xl mx-auto p-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-3 bg-white rounded-xl">
              <Brain className="w-8 h-8 text-black" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">
                Hello, {userName}!
              </h1>
              <p className="text-gray-300">Let's discover your personality traits</p>
            </div>
          </div>

          <div className="mb-8">
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium text-gray-300">Question {currentQuestion + 1} of {questions.length}</span>
              <span className="text-sm font-medium text-white">{Math.round(progress)}% Complete</span>
            </div>
            <div className="w-full h-2 bg-black/30 rounded-full overflow-hidden">
              <div 
                className="h-full bg-white transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          <QuestionCard
            question={questions[currentQuestion]}
            currentAnswer={answers[currentQuestion]}
            onAnswer={handleAnswer}
          />

          <div className="flex justify-between gap-4 mt-8">
            {currentQuestion > 0 && (
              <button
                onClick={() => setCurrentQuestion(curr => curr - 1)}
                className="px-6 py-3 text-white border border-white rounded-xl hover:bg-white/10 transition-all duration-200 flex items-center gap-2"
              >
                <ChevronLeft className="w-4 h-4" />
                Previous
              </button>
            )}
            
            {currentQuestion < questions.length - 1 ? (
              <button
                onClick={() => setCurrentQuestion(curr => curr + 1)}
                disabled={answers[currentQuestion] === -1}
                className="ml-auto px-6 py-3 bg-white text-black rounded-xl hover:bg-gray-100 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                Next
                <ChevronRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isAnalyzing || answers[currentQuestion] === -1}
                className="ml-auto px-6 py-3 bg-white text-black rounded-xl hover:bg-gray-100 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    AI Analysis in Progress...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    View AI Analysis
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}