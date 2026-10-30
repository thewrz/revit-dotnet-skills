# Inherited guidance consistency

An independent Astra xhigh survey covered all 40 skills, 42 supporting references, six agent definitions and seven routing/metadata files at `6a2da52`. Findings were checked against upstream provenance, current primary documentation and portable probes. This is a conflict-oriented survey, not compilation of every inherited example or proof of Revit host behavior.

## Accepted corrections

- **Package updates:** remove/add discarded a conditional reference's asset metadata on SDKs 8.0.130 and 10.0.111. In-place updating preserved it in the probe. The absolute XML-editing ban also contradicted the skill's conditional/centralized examples. Prefer in-place CLI updates, allow required XML changes, then inspect evaluated configurations and deployment assets. [Microsoft CLI contract](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-add), [reference metadata](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files).
- **Startup validation:** a bare provider did not invoke registered options validation in .NET 8 or 10 probes; explicit startup validation rejected invalid settings. Identify the startup owner instead of requiring a Generic Host in an add-in. [.NET registration](https://github.com/dotnet/runtime/blob/v10.0.0/src/libraries/Microsoft.Extensions.Options/src/OptionsBuilderExtensions.cs), [Generic Host invocation](https://github.com/dotnet/runtime/blob/v10.0.0/src/libraries/Microsoft.Extensions.Hosting/src/Internal/Host.cs).
- **Serialization:** remove the residual claim that Newtonsoft emits CLR names by default. A 13.0.3 probe confirmed default output omits them and opt-in `TypeNameHandling.All` includes them. [Official default](https://www.newtonsoft.com/json/help/html/P_Newtonsoft_Json_JsonSerializerSettings_TypeNameHandling.htm).
- **Companion services:** keep the intentional explicit-configuration policy, and distinguish it from discovery-enabled ServiceDefaults. Customize the package and registrations together. [Customizable defaults](https://aspire.dev/get-started/csharp-service-defaults/).

## Retained practices and limits

CPM, shared versions, explicit configuration and explicit serialization contracts remain intentional choices. Existing Revit-first routing already limits server, worker-thread, AOT and deployment examples to appropriate boundaries; their presence alone is not a conflict. A pinned compiler with an intentional language setting was not replaced merely because Microsoft's default differs.

Focused blind package-update and bare-provider startup baselines both produced correct implementations before these corrections. Both paired candidates also pass: conditional versions/assets remain intact, default/named validation precedes command exposure, and failed initialization disposes owned resources. These four one-sample checks establish preserved outcomes, not improved reliability. Mechanism probes establish the factual corrections. No proprietary source, project identities or research logs belong in this record.
