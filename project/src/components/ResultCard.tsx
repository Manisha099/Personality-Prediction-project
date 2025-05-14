import React, { useState } from 'react';
import { RefreshCw, Brain, ArrowRight } from 'lucide-react';
import type { PersonalityResult } from './types';
import { useSpring, animated } from 'react-spring';
import PersonalityDetailPage from './PersonalityDetailPage';
import { getPersonalityInsights } from '../utils/personalityInsights';

interface ResultCardProps {
  result: PersonalityResult;
  onReset: () => void;
}

export default function ResultCard({ result, onReset }: ResultCardProps) {
  const [selectedTrait, setSelectedTrait] = useState<string | null>(null);
  const [showDetail, setShowDetail] = useState(false);

  const fadeIn = useSpring({
    from: { opacity: 0, transform: 'translateY(20px)' },
    to: { opacity: 1, transform: 'translateY(0)' },
    config: { tension: 300, friction: 20 }
  });

  if (showDetail && selectedTrait) {
    const traitData = result.traits[selectedTrait];
    const insights = getPersonalityInsights(traitData.name, traitData.score);
    
    return (
      <PersonalityDetailPage
        trait={traitData}
        score={traitData.score}
        insights={insights}
        onBack={() => setShowDetail(false)}
      />
    );
  }

  const dominantTrait = result.traits[result.dominantTrait];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black py-12">
      <animated.div style={fadeIn} className="max-w-4xl mx-auto p-6 space-y-8">
        <div className="bg-white rounded-2xl p-8 shadow-xl">
          <div className="flex items-center gap-4 mb-8">
            <div className="p-3 bg-black rounded-xl">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-bold">Your Personality Analysis</h2>
              <p className="text-gray-600">Click on each trait to explore detailed insights</p>
            </div>
          </div>

          <div className="mb-8 p-6 bg-gradient-to-r from-gray-900 to-black rounded-xl text-white">
            <h3 className="text-xl mb-4">
              {result.userName}, {dominantTrait.name} is your dominant trait!
            </h3>
            <p className="text-lg mb-4">{result.summary}</p>
            <button
              onClick={() => {
                setSelectedTrait(result.dominantTrait);
                setShowDetail(true);
              }}
              className="flex items-center gap-2 text-white/80 hover:text-white transition-colors"
            >
              Click to explore your {dominantTrait.name} personality
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {Object.entries(result.traits).map(([trait, data]) => (
              <button
                key={trait}
                onClick={() => {
                  setSelectedTrait(trait);
                  setShowDetail(true);
                }}
                className={`p-6 rounded-xl transition-all duration-300 hover:scale-105 ${
                  data.color} text-white shadow-lg relative overflow-hidden`
                }
              >
                {trait === result.dominantTrait && (
                  <div className="absolute top-2 right-2 bg-white/20 px-2 py-1 rounded-full text-xs">
                    Dominant Trait
                  </div>
                )}
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold">{data.name}</h3>
                  <span className="text-2xl font-bold">{data.score}%</span>
                </div>
                <p className="text-sm text-white/90">
                  {data.description}
                </p>
                <div className="w-full bg-black/20 rounded-full h-2 mt-4">
                  <div 
                    className="h-full bg-white rounded-full transition-all duration-1000"
                    style={{ width: `${data.score}%` }}
                  />
                </div>
              </button>
            ))}
          </div>

          <button
            onClick={onReset}
            className="w-full bg-black text-white py-4 px-6 rounded-xl font-semibold hover:bg-gray-900 transition-all duration-200 flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-5 h-5" />
            Take Test Again
          </button>
        </div>
      </animated.div>
    </div>
  );
}