export interface Question {
  text: string;
  options: string[];
  trait: 'openness' | 'conscientiousness' | 'extraversion' | 'agreeableness' | 'neuroticism';
  direction: 1 | -1;
}

export interface TraitResult {
  name: string;
  description: string;
  score: number;
  details: string;
  color: string;
}

export interface PersonalityResult {
  summary: string;
  dominantTrait: string;
  userName: string;
  traits: {
    openness: TraitResult;
    conscientiousness: TraitResult;
    extraversion: TraitResult;
    agreeableness: TraitResult;
    neuroticism: TraitResult;
  };
}