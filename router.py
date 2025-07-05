#!/usr/bin/env python3
"""
Resonanz-Trichord Router - Event routing system for Quen-3-8B, Phi-4-Mini, and GPT-4.1
Implements metabolic Divergenz–Resonanz–Integration loop with marker-driven flow control.
"""

import asyncio
import logging
import websockets
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from ruamel.yaml import YAML

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('router.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ModelConfig:
    """Immutable model configuration"""
    name: str
    role: str
    endpoint: str
    tasks: List[str]
    context_size_tokens: Optional[int] = None

@dataclass(frozen=True)
class PhaseThresholds:
    """Immutable phase transition thresholds"""
    fluegel_to_strudel: float
    strudel_to_knoten: float
    knoten_to_kristall: float

@dataclass(frozen=True)
class RoleConfig:
    """Immutable role configuration"""
    model_ref: str
    allowed_markers: List[str]

@dataclass(frozen=True)
class RouterPolicy:
    """Immutable router policy configuration"""
    flow_control: str
    fallback_logic: str
    archetype_switching: bool
    max_chain_depth: int
    synergy_cooldown_seconds: int

@dataclass(frozen=True)
class SelfTuning:
    """Immutable self-tuning configuration"""
    update_source: str
    cadence: str
    update_parameters: List[str]

@dataclass(frozen=True)
class SynergyWeights:
    """Immutable synergy weight configuration"""
    positive: Dict[str, float]
    negative: Dict[str, float]

@dataclass(frozen=True)
class Debugging:
    """Immutable debugging configuration"""
    enable_logging: bool
    log_level: str
    log_file: str

@dataclass(frozen=True)
class RouterConfig:
    """Immutable router configuration"""
    metadata: Dict[str, Any]
    models: Dict[str, ModelConfig]
    phase_thresholds: PhaseThresholds
    roles: Dict[str, RoleConfig]
    router_policy: RouterPolicy
    self_tuning: SelfTuning
    synergy_weights: SynergyWeights
    debugging: Debugging

class Router:
    """
    Resonanz-Trichord Router implementing marker-driven flow control
    with metabolic Divergenz–Resonanz–Integration loop.
    """
    
    def __init__(self, config: RouterConfig):
        self.config = config
        self.current_phase = "divergenz"
        self.chain_depth = 0
        self.last_synergy_time = datetime.now()
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging based on configuration"""
        if self.config.debugging.enable_logging:
            log_level = getattr(logging, self.config.debugging.log_level.upper())
            logger.setLevel(log_level)
    
    def route(self, event: Dict[str, Any]) -> str:
        """
        Route event to appropriate model based on current phase and markers.
        
        Args:
            event: Event dictionary containing text and metadata
            
        Returns:
            str: Chosen model name
        """
        try:
            # Extract markers from event text
            text = event.get('text', '')
            markers = self._extract_markers(text)
            
            # Determine phase based on markers and thresholds
            phase = self._determine_phase(markers, event)
            
            # Get role configuration for current phase
            role_config = self.config.roles.get(phase)
            if not role_config:
                logger.warning(f"Unknown phase: {phase}, falling back to divergenz")
                phase = "divergenz"
                role_config = self.config.roles[phase]
            
            # Get model reference
            model_ref = role_config.model_ref
            model_config = self.config.models.get(model_ref)
            
            if not model_config:
                logger.error(f"Model reference {model_ref} not found")
                return "primary"  # Fallback
            
            # Check synergy weights
            synergy_factor = self._calculate_synergy_factor(markers)
            if synergy_factor != 1.0:
                logger.info(f"Synergy factor applied: {synergy_factor}")
            
            # Update chain depth
            self.chain_depth += 1
            if self.chain_depth > self.config.router_policy.max_chain_depth:
                logger.warning("Max chain depth reached, resetting")
                self.chain_depth = 0
            
            logger.info(f"Routed to {model_config.name} (phase: {phase}, markers: {markers})")
            return model_config.name
            
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return "primary"  # Fallback to primary model
    
    def update_thresholds(self, delta: Dict[str, float]) -> None:
        """
        Apply weekly tuning deltas to phase thresholds.
        
        Args:
            delta: Dictionary of threshold adjustments
        """
        try:
            # Create new phase thresholds with applied deltas
            current_thresholds = self.config.phase_thresholds
            
            new_fluegel = current_thresholds.fluegel_to_strudel + delta.get('fluegel_to_strudel', 0.0)
            new_strudel = current_thresholds.strudel_to_knoten + delta.get('strudel_to_knoten', 0.0)
            new_knoten = current_thresholds.knoten_to_kristall + delta.get('knoten_to_kristall', 0.0)
            
            # Clamp values to reasonable bounds
            new_fluegel = max(0.0, min(1.0, new_fluegel))
            new_strudel = max(0.0, min(1.0, new_strudel))
            new_knoten = max(0.0, min(1.0, new_knoten))
            
            # Create new config with updated thresholds
            new_thresholds = PhaseThresholds(
                fluegel_to_strudel=new_fluegel,
                strudel_to_knoten=new_strudel,
                knoten_to_kristall=new_knoten
            )
            
            # Update config (in real implementation, this would be more sophisticated)
            self.config = RouterConfig(
                metadata=self.config.metadata,
                models=self.config.models,
                phase_thresholds=new_thresholds,
                roles=self.config.roles,
                router_policy=self.config.router_policy,
                self_tuning=self.config.self_tuning,
                synergy_weights=self.config.synergy_weights,
                debugging=self.config.debugging
            )
            
            logger.info(f"Updated thresholds: {new_thresholds}")
            
        except Exception as e:
            logger.error(f"Error updating thresholds: {e}")
    
    def export_yaml(self) -> str:
        """
        Export current router state to YAML format.
        
        Returns:
            str: YAML representation of current configuration
        """
        try:
            yaml = YAML()
            yaml.default_flow_style = False
            
            # Convert dataclasses to dictionaries
            export_data = {
                'resonanz_trichord_router': {
                    'metadata': self.config.metadata,
                    'models': {
                        name: {
                            'name': model.name,
                            'role': model.role,
                            'endpoint': model.endpoint,
                            'tasks': model.tasks,
                            **({'context_size_tokens': model.context_size_tokens} if model.context_size_tokens else {})
                        }
                        for name, model in self.config.models.items()
                    },
                    'phase_thresholds': {
                        'fluegel_to_strudel': self.config.phase_thresholds.fluegel_to_strudel,
                        'strudel_to_knoten': self.config.phase_thresholds.strudel_to_knoten,
                        'knoten_to_kristall': self.config.phase_thresholds.knoten_to_kristall
                    },
                    'roles': {
                        name: {
                            'model_ref': role.model_ref,
                            'allowed_markers': role.allowed_markers
                        }
                        for name, role in self.config.roles.items()
                    },
                    'router_policy': {
                        'flow_control': self.config.router_policy.flow_control,
                        'fallback_logic': self.config.router_policy.fallback_logic,
                        'archetype_switching': self.config.router_policy.archetype_switching,
                        'max_chain_depth': self.config.router_policy.max_chain_depth,
                        'synergy_cooldown_seconds': self.config.router_policy.synergy_cooldown_seconds
                    },
                    'self_tuning': {
                        'update_source': self.config.self_tuning.update_source,
                        'cadence': self.config.self_tuning.cadence,
                        'update_parameters': self.config.self_tuning.update_parameters
                    },
                    'synergy_weights': {
                        'positive': self.config.synergy_weights.positive,
                        'negative': self.config.synergy_weights.negative
                    },
                    'debugging': {
                        'enable_logging': self.config.debugging.enable_logging,
                        'log_level': self.config.debugging.log_level,
                        'log_file': self.config.debugging.log_file
                    }
                }
            }
            
            # Convert to string
            from io import StringIO
            stream = StringIO()
            yaml.dump(export_data, stream)
            return stream.getvalue()
            
        except Exception as e:
            logger.error(f"Error exporting YAML: {e}")
            return ""
    
    def _extract_markers(self, text: str) -> List[str]:
        """
        Extract semantic markers from text.
        
        TODO: Implement marker extraction logic based on semantic analysis
        """
        # Placeholder implementation
        markers = []
        text_lower = text.lower()
        
        # Simple keyword-based marker extraction
        marker_keywords = {
            'Flügel': ['flügel', 'fluegel', 'wing'],
            'Überraschung': ['überraschung', 'ueberraschung', 'surprise'],
            'Kind_Ich': ['kind', 'ich', 'child', 'self'],
            'Strudel': ['strudel', 'whirl', 'vortex'],
            'Schatten': ['schatten', 'shadow'],
            'Wut': ['wut', 'anger', 'rage'],
            'Furcht': ['furcht', 'fear', 'angst'],
            'Kristalle': ['kristalle', 'crystal'],
            'Vertrauen': ['vertrauen', 'trust'],
            'Beobachter': ['beobachter', 'observer']
        }
        
        for marker, keywords in marker_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                markers.append(marker)
        
        return markers
    
    def _determine_phase(self, markers: List[str], event: Dict[str, Any]) -> str:
        """
        Determine current phase based on markers and thresholds.
        """
        # Calculate marker scores
        divergenz_score = sum(1 for marker in markers if marker in ['Flügel', 'Überraschung', 'Kind_Ich'])
        resonanz_score = sum(1 for marker in markers if marker in ['Strudel', 'Schatten', 'Wut', 'Furcht'])
        integration_score = sum(1 for marker in markers if marker in ['Kristalle', 'Vertrauen', 'Beobachter'])
        
        # Normalize scores
        total_markers = len(markers) if markers else 1
        divergenz_ratio = divergenz_score / total_markers
        resonanz_ratio = resonanz_score / total_markers
        integration_ratio = integration_score / total_markers
        
        # Phase transition logic
        if integration_ratio >= self.config.phase_thresholds.knoten_to_kristall:
            return "integration"
        elif resonanz_ratio >= self.config.phase_thresholds.strudel_to_knoten:
            return "resonanz"
        elif divergenz_ratio >= self.config.phase_thresholds.fluegel_to_strudel:
            return "divergenz"
        else:
            return "divergenz"  # Default phase
    
    def _calculate_synergy_factor(self, markers: List[str]) -> float:
        """
        Calculate synergy factor based on marker combinations.
        """
        if not markers or len(markers) < 2:
            return 1.0
        
        synergy_factor = 1.0
        
        # Check positive synergies
        for combo, weight in self.config.synergy_weights.positive.items():
            marker1, marker2 = combo.split('+')
            if marker1 in markers and marker2 in markers:
                synergy_factor *= weight
        
        # Check negative synergies
        for combo, weight in self.config.synergy_weights.negative.items():
            marker1, marker2 = combo.split('+')
            if marker1 in markers and marker2 in markers:
                synergy_factor *= (1 + weight)  # weight is negative
        
        return synergy_factor

async def send_to_model(model_name: str, message: str, endpoint: str) -> str:
    """
    Send message to model via WebSocket.
    
    TODO: Implement WebSocket bus integration
    """
    try:
        # Placeholder WebSocket implementation
        logger.info(f"Sending to {model_name} at {endpoint}: {message[:50]}...")
        
        # TODO: Implement actual WebSocket communication
        # async with websockets.connect(endpoint) as websocket:
        #     await websocket.send(message)
        #     response = await websocket.recv()
        #     return response
        
        return f"Response from {model_name}: {message}"
        
    except Exception as e:
        logger.error(f"Error sending to {model_name}: {e}")
        return f"Error: {e}"

def load_router_config(yaml_file: str) -> RouterConfig:
    """
    Load router configuration from YAML file.
    
    Args:
        yaml_file: Path to YAML configuration file
        
    Returns:
        RouterConfig: Loaded configuration
    """
    try:
        yaml = YAML()
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
        
        router_data = data.get('resonanz_trichord_router', {})
        
        # Parse models
        models = {}
        for name, model_data in router_data.get('models', {}).items():
            models[name] = ModelConfig(
                name=model_data['name'],
                role=model_data['role'],
                endpoint=model_data['endpoint'],
                tasks=model_data['tasks'],
                context_size_tokens=model_data.get('context_size_tokens')
            )
        
        # Parse phase thresholds
        thresholds_data = router_data.get('phase_thresholds', {})
        phase_thresholds = PhaseThresholds(
            fluegel_to_strudel=thresholds_data.get('fluegel_to_strudel', 0.25),
            strudel_to_knoten=thresholds_data.get('strudel_to_knoten', 0.60),
            knoten_to_kristall=thresholds_data.get('knoten_to_kristall', 0.30)
        )
        
        # Parse roles
        roles = {}
        for name, role_data in router_data.get('roles', {}).items():
            roles[name] = RoleConfig(
                model_ref=role_data['model_ref'],
                allowed_markers=role_data['allowed_markers']
            )
        
        # Parse router policy
        policy_data = router_data.get('router_policy', {})
        router_policy = RouterPolicy(
            flow_control=policy_data.get('flow_control', 'marker_driven'),
            fallback_logic=policy_data.get('fallback_logic', 'RD + Drift_Δ'),
            archetype_switching=policy_data.get('archetype_switching', True),
            max_chain_depth=policy_data.get('max_chain_depth', 3),
            synergy_cooldown_seconds=policy_data.get('synergy_cooldown_seconds', 30)
        )
        
        # Parse self tuning
        tuning_data = router_data.get('self_tuning', {})
        self_tuning = SelfTuning(
            update_source=tuning_data.get('update_source', 'archive_fallback'),
            cadence=tuning_data.get('cadence', 'RRULE:FREQ=WEEKLY;BYDAY=MO;BYHOUR=03;BYMINUTE=00'),
            update_parameters=tuning_data.get('update_parameters', ['phase_thresholds', 'synergy_weights'])
        )
        
        # Parse synergy weights
        weights_data = router_data.get('synergy_weights', {})
        synergy_weights = SynergyWeights(
            positive=weights_data.get('positive', {}),
            negative=weights_data.get('negative', {})
        )
        
        # Parse debugging
        debug_data = router_data.get('debugging', {})
        debugging = Debugging(
            enable_logging=debug_data.get('enable_logging', True),
            log_level=debug_data.get('log_level', 'INFO'),
            log_file=debug_data.get('log_file', 'router.log')
        )
        
        return RouterConfig(
            metadata=router_data.get('metadata', {}),
            models=models,
            phase_thresholds=phase_thresholds,
            roles=roles,
            router_policy=router_policy,
            self_tuning=self_tuning,
            synergy_weights=synergy_weights,
            debugging=debugging
        )
        
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

def main():
    """Demo function that loads configuration and routes a sample event."""
    try:
        # Load configuration
        config = load_router_config('resonanz_trichord_router.yaml')
        
        # Create router
        router = Router(config)
        
        # Sample events to test routing
        sample_events = [
            {
                'text': 'Ich fühle mich wie ein Kind und bin überrascht von der Situation.',
                'metadata': {'user_id': 'test_user_1'}
            },
            {
                'text': 'Es gibt einen Strudel von Wut und Schatten in mir.',
                'metadata': {'user_id': 'test_user_2'}
            },
            {
                'text': 'Ich sehe Kristalle des Vertrauens und bin ein Beobachter.',
                'metadata': {'user_id': 'test_user_3'}
            }
        ]
        
        print("🧠 Resonanz-Trichord Router Demo")
        print("=" * 50)
        
        for i, event in enumerate(sample_events, 1):
            print(f"\nEvent {i}: {event['text']}")
            chosen_model = router.route(event)
            print(f"Routed to: {chosen_model}")
        
        # Test threshold update
        print(f"\nUpdating thresholds...")
        router.update_thresholds({
            'fluegel_to_strudel': 0.1,
            'strudel_to_knoten': -0.1,
            'knoten_to_kristall': 0.05
        })
        
        # Export current state
        yaml_export = router.export_yaml()
        print(f"\nExported YAML length: {len(yaml_export)} characters")
        
    except FileNotFoundError:
        print("❌ Configuration file 'resonanz_trichord_router.yaml' not found")
        print("Please create the YAML configuration file first.")
    except Exception as e:
        print(f"❌ Error in demo: {e}")

if __name__ == "__main__":
    main() 