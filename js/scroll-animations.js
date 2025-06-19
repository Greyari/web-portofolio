
// Animate project cards
gsap.utils.toArray('.project-card').forEach((card, i) => {
    gsap.fromTo(card, 
        { opacity: 0, y: 50 },
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
                trigger: card,
                start: "top 80%",
                toggleActions: "play none none none"
            }
        }
    );
});

// Animate skill cards
gsap.utils.toArray('.skill-card').forEach((card, i) => {
    gsap.fromTo(card, 
        { opacity: 0, y: 50 },
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
                trigger: card,
                start: "top 80%",
                toggleActions: "play none none none"
            }
        }
    );
});

// Animate interest cards
gsap.utils.toArray('.interest-card').forEach((card, i) => {
    gsap.fromTo(card, 
        { opacity: 0, y: 50 },
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
                trigger: card,
                start: "top 80%",
                toggleActions: "play none none none"
            }
        }
    );
});

// Section title animations
gsap.utils.toArray('section h2').forEach((title) => {
    gsap.fromTo(title, 
        { opacity: 0, y: 30 },
        {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: "power3.out",

        }
    );
    
    // Animate the colored span separately
    const span = title.querySelector('span');
    if (span) {
        gsap.fromTo(span, 
            { opacity: 0, x: -20 },
            {
                opacity: 1,
                x: 0,
                duration: 1,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: title,
                    start: "top 80%",
                    toggleActions: "play none none none"
                }
            }
        );
    }
});

// Contact section animation
gsap.fromTo('#contact', 
    { opacity: 0 },
    {
        opacity: 1,
        scrollTrigger: {
            trigger: '#contact',
            start: "top 80%",
            toggleActions: "play none none none",
            onEnter: () => {
                gsap.fromTo('.contact-info', 
                    { opacity: 0, x: -50 },
                    { opacity: 1, x: 0, duration: 0.8, ease: "power2.out" }
                );
                gsap.fromTo('.contact-form', 
                    { opacity: 0, x: 50 },
                    { opacity: 1, x: 0, duration: 0.8, ease: "power2.out" }
                );
            }
        }
    }
);