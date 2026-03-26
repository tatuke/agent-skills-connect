#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import Any, Type

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class WorkflowEngine:
    """
    Generic workflow engine that routes data between skills based on their input/output type signatures.
    """
    def __init__(self):
        self.registered_skills = []

    def register(self, skill_instance):
        self.registered_skills.append(skill_instance)

    def _find_skill(self, input_type: Type) -> Any:
        for skill in self.registered_skills:
            if getattr(skill, 'input_signature', None) == input_type:
                return skill
        return None

    def execute(self, initial_data: Any) -> Any:
        logger.info("Starting generic workflow execution...")
        current_data = initial_data

        while True:
            current_type = type(current_data)
            next_skill = self._find_skill(current_type)

            if next_skill:
                logger.info(f"Routing {current_type.__name__} to: {getattr(next_skill, 'name', next_skill.__class__.__name__)}")
                current_data = next_skill.run(current_data)
                continue
            
            # Handle list/iterable unwrapping automatically
            if isinstance(current_data, list) or (hasattr(current_data, 'items') and isinstance(current_data.items, list)):
                iterable_data = current_data if isinstance(current_data, list) else current_data.items
                
                if not iterable_data:
                    logger.info("Empty iterable encountered. Terminating workflow.")
                    break
                
                item_type = type(iterable_data[0])
                next_skill = self._find_skill(item_type)
                
                if next_skill:
                    logger.info(f"Unpacking iterable of {item_type.__name__} to: {getattr(next_skill, 'name', next_skill.__class__.__name__)}")
                    results = [next_skill.run(item) for item in iterable_data]
                    current_data = results
                    continue
            
            logger.info(f"Workflow finished. Final output type: {type(current_data).__name__}")
            break
            
        return current_data
