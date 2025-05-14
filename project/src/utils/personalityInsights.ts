export const getPersonalityInsights = (trait: string, score: number) => {
  const insights = {
    'openness to experience': {
      strengths: [
        "Creative problem-solving abilities",
        "Strong appreciation for art and beauty",
        "Intellectual curiosity and love of learning",
        "Ability to think abstractly and see multiple perspectives"
      ],
      challenges: [
        "May struggle with routine tasks",
        "Can be easily distracted by new ideas",
        "Might have difficulty with practical matters"
      ],
      careerPaths: [
        "Artist or Creative Professional",
        "Researcher or Scientist",
        "Innovation Consultant",
        "Writer or Content Creator"
      ],
      relationships: "You thrive in relationships that offer intellectual stimulation and creative freedom. You appreciate partners who can engage in deep conversations and share your curiosity about life.",
      growthAreas: [
        "Balancing creativity with practicality",
        "Developing focus on immediate tasks",
        "Setting realistic goals alongside creative pursuits"
      ]
    },
    'conscientiousness': {
      strengths: [
        "Excellent organizational skills",
        "Strong work ethic and reliability",
        "Attention to detail",
        "Goal-oriented mindset"
      ],
      challenges: [
        "May be perceived as inflexible",
        "Tendency to overwork",
        "Perfectionist tendencies"
      ],
      careerPaths: [
        "Project Manager",
        "Financial Analyst",
        "Quality Assurance Specialist",
        "Business Administrator"
      ],
      relationships: "You value reliability and consistency in relationships. You appreciate partners who are responsible and share your commitment to long-term goals.",
      growthAreas: [
        "Developing flexibility in approaches",
        "Learning to delegate tasks",
        "Finding balance between work and relaxation"
      ]
    },
    'extraversion': {
      strengths: [
        "Natural networking abilities",
        "Strong communication skills",
        "Energy and enthusiasm",
        "Leadership potential"
      ],
      challenges: [
        "May find it difficult to work alone",
        "Can be overwhelmed by too much quiet time",
        "Might struggle with deep focus tasks"
      ],
      careerPaths: [
        "Sales Representative",
        "Public Relations Specialist",
        "Event Planner",
        "Teacher or Trainer"
      ],
      relationships: "You thrive in social situations and enjoy building connections. You seek partners who can match your energy and enjoy an active social life.",
      growthAreas: [
        "Developing comfort with solitude",
        "Practicing active listening",
        "Building depth in relationships"
      ]
    },
    'agreeableness': {
      strengths: [
        "Strong empathy and compassion",
        "Excellent team player",
        "Natural mediator",
        "Trustworthy and reliable"
      ],
      challenges: [
        "May have difficulty saying no",
        "Can be too self-sacrificing",
        "Might avoid necessary conflict"
      ],
      careerPaths: [
        "Counselor or Therapist",
        "Human Resources Professional",
        "Social Worker",
        "Healthcare Provider"
      ],
      relationships: "You excel at creating harmonious relationships and understanding others' needs. You value emotional connection and mutual support in partnerships.",
      growthAreas: [
        "Setting healthy boundaries",
        "Developing assertiveness",
        "Balancing others' needs with your own"
      ]
    },
    'emotional stability': {
      strengths: [
        "High self-awareness",
        "Attention to potential problems",
        "Emotional depth and sensitivity",
        "Strong risk assessment abilities"
      ],
      challenges: [
        "May experience anxiety or stress",
        "Can be sensitive to criticism",
        "Might overthink decisions"
      ],
      careerPaths: [
        "Risk Analyst",
        "Quality Control Specialist",
        "Editor or Proofreader",
        "Safety Coordinator"
      ],
      relationships: "You bring depth and emotional awareness to relationships. You appreciate partners who can provide stability and understanding during stressful times.",
      growthAreas: [
        "Building emotional resilience",
        "Developing stress management techniques",
        "Practicing positive self-talk"
      ]
    }
  };

  return insights[trait.toLowerCase()] || insights['emotional stability'];
};