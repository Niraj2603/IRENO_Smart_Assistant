# Generative AI-based Assistant Solution for IRENO Platform

## 1. Introduction
This document outlines the scope for developing a Generative AI-based assistant solution to be integrated with the IRENO platform—Intuitive Response Enabled Network Operations.  
IRENO is a unified platform that extracts actionable insights from electric utility IT-OT systems, offering a single pane of glass for network operators, field technicians, and leadership teams. It integrates IT-OT systems to deliver real-time insights, predictive analytics, and operational control. With GenAI infusion, IRENO will be able to consume information from smart meter operations, storm management, DER optimization, and more in an easy to consume fashion.

## 2. Objective
To build a natural language interface powered by Generative AI that enables users to:
- Discover and retrieve information across electric utility systems.
- Summarize and contextualize data.
- Generate reports and insights.
- Enhance decision-making and operational efficiency.

## 3. Target Audience
- **Field Technicians**: For real-time fault detection and resolution.
- **Command Center Operators**: For situational awareness and operational control.
- **Senior Leadership**: For strategic insights and performance monitoring.

## 4. Platform and Technology Stack
- **Frontend**: Java-based UI using frameworks like React (team discretion).
- **Backend**: J2EE stack with secure APIs.
- **Architecture**: Three-tier (UI, backend services, optional datastore).
- **LLM Integration**: API-based access to models like LLaMA, Claude, etc.
- **Data Sources**: IRENO API and Document Repository API.

## 5. Requirements

### 5.1. User Requirements
1. Ability to type natural language queries.  
2. Receive summarized responses and actionable insights.  
3. Generate downloadable reports.  
4. View historical prompts and context.  

### 5.2. UI Requirements
- WCAG 2.1 compliance.  
- Responsive design for desktop and mobile.  
- Intuitive UI with minimal learning curve.  
- Multilingual support (optional).  

### 5.3. Security Requirements
- Login Mechanism  
- Secure API communication (OAuth2, JWT).  
- Data encryption at rest and in transit.  
- Compliance with enterprise security policies.  

## 6. Deliverables
- Responsive UI with chat interface.  
- Backend orchestration engine for query routing and context management.  
- Integration with LLM endpoint.  
- Secure connectors to IRENO and document repository APIs.  
- Optional datastore for prompt history and context caching.  

## 7. Acceptance Criteria
- Successful integration with IRENO and document repository APIs.  
- Accurate context detection and routing by LLM.  
- UI responsiveness across devices.  
- Security audit clearance.  
- Positive feedback from pilot users.  

## 8. Conclusion
This assistant will enhance IRENO’s capabilities by enabling intuitive, AI-powered interactions. It aligns with IRENO’s vision of predictive, prescriptive, and proactive network operations.

# Copilot Instructions for IRENO Smart Assistant

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a React JavaScript project for IRENO Smart Assistant - a ChatGPT-style AI interface for electric utilities.

## Key Technologies
- React (JavaScript)
- Vite (build tool)
- React Router (navigation)
- CSS Modules (styling)
- Lucide React (icons)

## Project Structure
- Components are organized in `src/components/`
- Pages are in `src/pages/`
- Styles use CSS modules with `.module.css` extension
- Context/hooks for state management in `src/context/`

## Coding Guidelines
- Use functional components with React hooks
- Follow React best practices
- Use CSS modules for component styling
- Maintain the same UI/UX as the original HTML/CSS version
- Keep components modular and reusable
- Use proper semantic HTML elements
- Ensure accessibility standards

## Features to Implement
- Login page with role selection
- Main chat interface
- Sidebar with conversation history
- Theme toggle (light/dark)
- Modal components (settings, sharing)
- Responsive design
- Voice input support
- File upload functionality

