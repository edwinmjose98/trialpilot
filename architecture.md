Protocol
├── VisitDefinitions (protocol_id FK)
│   └── ProcedureDefinitions (visit_definition_id FK)
├── EligibilityCriteria (protocol_id FK)
├── Patients (protocol_id FK)
│   └── VisitSchedule (patient_id FK)
│       └── ChecklistItems (visit_schedule_id FK)
└── Alerts (protocol_id FK)