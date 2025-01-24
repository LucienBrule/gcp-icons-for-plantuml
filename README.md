# GCP Icons for PlantUML

PlantUML macros and sprites for Google Cloud Platform (GCP) services. Easily create professional diagrams with GCP components for architecture, workflows, and network topologies.

---

## 🚀 Quick Start

Add the GCP icons to your PlantUML project by including the following line in your `.puml` file:

```plantuml
!includeurl https://raw.githubusercontent.com/LucienBrule/gcp-icons-for-plantuml/master/dist/GCPCommon.puml
```

You can include icons for specific services or categories. For example:

```plantuml
!includeurl https://raw.githubusercontent.com/LucienBrule/gcp-icons-for-plantuml/master/dist/ai_platform/ai_platform.puml
!includeurl https://raw.githubusercontent.com/LucienBrule/gcp-icons-for-plantuml/master/dist/anthos_config_management/anthos_config_management.puml
```

---

## 📄 Example Diagram

```plantuml
@startuml HelloWorld

' Include common macros and service-specific macros
!includeurl https://raw.githubusercontent.com/LucienBrule/gcp-icons-for-plantuml/master/dist/GCPCommon.puml
!includeurl https://raw.githubusercontent.com/LucienBrule/gcp-icons-for-plantuml/master/dist/ai_platform/ai_platform.puml
!includeurl https://raw.githubusercontent.com/LucienBrule/gcp-icons-for-plantuml/master/dist/anthos_config_management/anthos_config_management.puml

LAYOUT_LEFT_RIGHT

actor "Developer" as dev

ai_platform(aiAlias, "AI Platform", "Training & Serving")
anthos_config_management(cfgAlias, "Anthos Config Management", "Policy as Code", "Enforces governance")

dev --> aiAlias : triggers job
aiAlias --> cfgAlias : fetches config

@enduml
```

You can view a listing of all available services and categories in the `dist/` directory.
Or if you want to see a table of all available services and categories, you can view the [GCP Services and Categories](dist/GCPSymbols.md)

---

## ✨ Output Example

This code generates the following diagram:

![HelloWorld Example](http://www.plantuml.com/plantuml/proxy?&src=https://raw.github.com/LucienBrule/gcp-icons-for-plantuml/blob/master/examples/HelloWorld.puml)

---

## 🗂 Directory Structure

- **`dist/`**: Contains the generated `.puml` files for each GCP service and category.
- **`examples/`**: Ready-to-use PlantUML examples for testing and inspiration.
- **`benchmark/`**: Complex diagrams generated for performance and visualization benchmarking.

---

## 🛠 Contributing

We welcome contributions! Feel free to open issues or pull requests to add new features or fix bugs. See `CONTRIBUTING.md` for guidelines.

---

## 📜 License

This project is licensed under the MIT License for the code, and the CC-BY-ND 2.0 License for the icons.