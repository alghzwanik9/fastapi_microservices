# Common Utilities Library

This directory contains shared utilities and middleware used across all microservices.

## Structure

```
common/
├── utils/          # Utility functions
├── middleware/     # Custom middleware
└── events/         # Event handling and messaging
```

## Installation

The common library is installed as part of each service's dependencies.

## Usage

### Utils

```python
from common.utils import logging_config, validation_helpers
```

### Middleware

```python
from common.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware
```

### Events

```python
from common.events import EventPublisher, EventConsumer

publisher = EventPublisher()
publisher.publish('user.created', {'user_id': 123})
```
