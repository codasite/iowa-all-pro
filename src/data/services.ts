export type ServiceItem = {
  title: string;
  description: string;
  href: string;
  iconSymbol?: string;
};

export const services: ServiceItem[] = [
  {
    title: 'Duct Cleaning',
    description:
      'Dust and contaminants can accumulate in your ductwork over time, impacting the air you breathe. Our professional ductwork cleaning service removes these impurities, improving air quality and energy efficiency.',
    href: '/services/duct-cleaning',
    iconSymbol: 'Lineariconsicon-earth'
  },
  {
    title: 'Heating',
    description:
      "We get it - a broken furnace can disrupt your routine. That's why we prioritize swift service without compromising on quality. Our goal? Get your furnace back up and running ASAP.",
    href: '/services/heating',
    iconSymbol: 'FontAwesomeicon-fire'
  },
  {
    title: 'Cooling',
    description:
      "Taking care of your AC system and fixing it when needed saves money on energy bills and keeps you cool. We are committed to excellence, so we use high-quality parts and materials to repair your AC unit. This ensures long-lasting results.",
    href: '/services/cooling',
    iconSymbol: 'Lineariconsicon-home'
  },
  {
    title: 'Water Heaters',
    description:
      'Whether you need a new energy-efficient water heater installed or routine maintenance to extend the life of your current unit, our experts fix any issues.',
    href: '/water-heater-service',
    iconSymbol: 'Lineariconsicon-drop'
  },
  {
    title: 'Indoor Air Quality',
    description:
      'We offer a comprehensive range of indoor air quality solutions to ensure that your indoor environment remains clean, healthy, and enjoyable.',
    href: '/services/indoor-air-quality',
    iconSymbol: 'Lineariconsicon-cloud-sync'
  },
  {
    title: 'Commercial HVAC',
    description:
      'Trust Iowa All Pro for reliable, high-quality service that supports your business goals. Whether you manage an office, retail space, or industrial facility, we’re committed to keeping your HVAC system in peak condition.',
    href: '/services/commercial-hvac',
    iconSymbol: 'Lineariconsicon-apartment'
  }
];


