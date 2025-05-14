import React from 'react';
import type { Question } from './types';

interface QuestionCardProps {
  question: Question;
  currentAnswer: number;
  onAnswer: (value: number) => void;
}

export default function QuestionCard({ question, currentAnswer, onAnswer }: QuestionCardProps) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-white">{question.text}</h2>
      <div className="grid grid-cols-1 gap-3">
        {question.options.map((option, index) => (
          <button
            key={index}
            onClick={() => onAnswer(index)}
            className={`p-4 rounded-xl border-2 transition-all duration-200 text-left hover:shadow-md ${
              currentAnswer === index
                ? 'border-transparent bg-white text-black shadow-lg'
                : 'border-white/20 text-white hover:border-white/40 hover:bg-white/5'
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}