import React from 'react';
import { ArrowLeft, Brain, Sparkles, Target, Users, Heart, Shield } from 'lucide-react';
import { useSpring, animated } from 'react-spring';
import type { TraitResult } from './types';

interface PersonalityDetailPageProps {
  trait: TraitResult;
  score: number;
  insights: TraitInsights;
  onBack: () => void;
}

interface TraitInsights {
  strengths: string[];
  challenges: string[];
  careerPaths: string[];
  relationships: string;
  growthAreas: string[];
}

const getTraitIcon = (traitName: string) => {
  switch (traitName.toLowerCase()) {
    case 'openness to experience':
      return <Sparkles className="w-6 h-6" />;
    case 'conscientiousness':
      return <Target className="w-6 h-6" />;
    case 'extraversion':
      return <Users className="w-6 h-6" />;
    case 'agreeableness':
      return <Heart className="w-6 h-6" />;
    case 'emotional stability':
      return <Shield className="w-6 h-6" />;
    default:
      return <Brain className="w-6 h-6" />;
  }
};

const getQuickFacts = (score: number, traitName: string) => {
  const facts = [];
  
  if (score >= 80) {
    facts.push(`You have an exceptional capacity for ${traitName.toLowerCase()}`);
  } else if (score >= 60) {
    facts.push(`You show strong tendencies toward ${traitName.toLowerCase()}`);
  } else if (score >= 40) {
    facts.push(`You have a balanced approach to ${traitName.toLowerCase()}`);
  } else if (score >= 20) {
    facts.push(`You are selective about when to express ${traitName.toLowerCase()}`);
  } else {
    facts.push(`You take a cautious approach to ${traitName.toLowerCase()}`);
  }

  facts.push(`This trait influences ${score}% of your personality`);
  facts.push(`You express this trait in ${score > 50 ? 'most' : 'select'} situations`);

  return facts;
};

export default function PersonalityDetailPage({ trait, score, insights, onBack }: PersonalityDetailPageProps) {
  const fadeIn = useSpring({
    from: { opacity: 0, transform: 'translateY(20px)' },
    to: { opacity: 1, transform: 'translateY(0)' },
    config: { tension: 300, friction: 20 }
  });

  const scoreAnimation = useSpring({
    from: { number: 0 },
    to: { number: score },
    config: { duration: 1000 }
  });

  const quickFacts = getQuickFacts(score, trait.name);

  return (
    <div className={`min-h-screen ${trait.color} py-12 text-white`}>
      <animated.div style={fadeIn} className="max-w-4xl mx-auto p-6">
        <button
          onClick={onBack}
          className="mb-8 flex items-center gap-2 text-white/80 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Overview
        </button>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-xl border border-white/20">
          <div className="flex items-center gap-4 mb-8">
            <div className="p-4 bg-white rounded-xl">
              {getTraitIcon(trait.name)}
            </div>
            <div>
              <h1 className="text-4xl font-bold">{trait.name}</h1>
              <p className="text-xl text-white/80">{trait.description}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="col-span-2">
              <p className="text-xl leading-relaxed mb-6">{trait.details}</p>
              <animated.div className="text-6xl font-bold mb-2">
                {scoreAnimation.number.to(n => `${Math.floor(n)}%`)}
              </animated.div>
              <p className="text-white/80">Expression Level</p>
            </div>
            <div className="space-y-4">
              <div className="h-full bg-white/20 rounded-xl p-6">
                <h3 className="text-xl font-semibold mb-4">Personal Insights</h3>
                <ul className="space-y-3">
                  {quickFacts.map((fact, index) => (
                    <li key={index} className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-white" />
                      {fact}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-black/20 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">Your Strengths</h3>
              <ul className="space-y-3">
                {insights.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 rounded-full bg-white mt-2" />
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-black/20 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">Growth Areas</h3>
              <ul className="space-y-3">
                {insights.growthAreas.map((area, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 rounded-full bg-white mt-2" />
                    <span>{area}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-black/20 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">Recommended Career Paths</h3>
              <ul className="space-y-3">
                {insights.careerPaths.map((path, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 rounded-full bg-white mt-2" />
                    <span>{path}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-black/20 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">Relationship Dynamics</h3>
              <p className="leading-relaxed">{insights.relationships}</p>
            </div>
          </div>
        </div>
      </animated.div>
    </div>
  );
}