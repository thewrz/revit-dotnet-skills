---
name: serialization
description: Choose the right serialization format for .NET applications. Prefer schema-based formats (Protobuf, MessagePack) over reflection-based (Newtonsoft.Json). Use System.Text.Json with AOT source generators for JSON scenarios.
user-invocable: false
---

> **Revit scope:** For Revit work, first read [revit-development](../revit-development/SKILL.md). Apply this skill only within the selected host/runtime and API-context boundaries; server examples concern companion services. Institutional preferences below remain intentional.


# Serialization in .NET

## When to Use This Skill

Use this skill when:
- Choosing a serialization format for APIs, messaging, or persistence
- Migrating from Newtonsoft.Json to System.Text.Json
- Implementing AOT-compatible serialization
- Designing wire formats for distributed systems
- Optimizing serialization performance

---

## Schema-Based vs Reflection-Based

| Aspect | Schema-Based | Reflection-Based |
|--------|--------------|------------------|
| **Contract/type metadata** | Protobuf has an external schema; MessagePack commonly uses keyed contracts; System.Text.Json source generation creates compile-time metadata/code | Depends on serializer and configuration; reflection does not inherently put CLR type names in the payload |
| **Versioning** | Depends on format and contract rules | Depends on serializer settings and contract evolution |
| **Performance** | Depends on format, payload, options, and generated/runtime path | Depends on format, payload, and settings |
| **AOT compatibility** | Supported by selected generated/contract-based paths; verify the chosen package and configuration | Configuration- and library-dependent; verify trimming/AOT support |
| **Wire compatibility** | Depends on schema/contract evolution rules | Depends on explicit contract and polymorphism settings |

**Recommendation**: Use schema-based serialization for anything that crosses process boundaries.

---

## Format Recommendations

| Use Case | Recommended Format | Why |
|----------|-------------------|-----|
| **REST APIs** | System.Text.Json (source gen) | Standard, AOT-compatible |
| **gRPC** | Protocol Buffers | Native format, excellent versioning |
| **Actor messaging** | MessagePack or Protobuf | Compact, fast, version-safe |
| **Event sourcing** | Protobuf or MessagePack | Must handle old events forever |
| **Caching** | MessagePack | Compact, fast |
| **Configuration** | JSON (System.Text.Json) | Human-readable |
| **Logging** | JSON (System.Text.Json) | Structured, parseable |

### Formats to Avoid

| Format | Problem |
|--------|---------|
| **BinaryFormatter** | Security vulnerabilities, deprecated, never use |
| **Enabled CLR type-name metadata** | Couples payloads to CLR names; Newtonsoft.Json defaults to [`TypeNameHandling.None`](https://www.newtonsoft.com/json/help/html/P_Newtonsoft_Json_JsonSerializerSettings_TypeNameHandling.htm) |
| **DataContractSerializer** | Complex, poor versioning |
| **XML** | Verbose, slow, complex |

---

## System.Text.Json with Source Generators

For JSON serialization, use System.Text.Json with source generators for AOT compatibility and performance.

### Setup

```csharp
// Define a JsonSerializerContext with all your types
[JsonSerializable(typeof(Order))]
[JsonSerializable(typeof(OrderItem))]
[JsonSerializable(typeof(Customer))]
[JsonSerializable(typeof(List<Order>))]
[JsonSourceGenerationOptions(
    PropertyNamingPolicy = JsonKnownNamingPolicy.CamelCase,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull)]
public partial class AppJsonContext : JsonSerializerContext { }
```

### Usage

```csharp
// Serialize with context
var json = JsonSerializer.Serialize(order, AppJsonContext.Default.Order);

// Deserialize with context
var order = JsonSerializer.Deserialize(json, AppJsonContext.Default.Order);

// Configure in ASP.NET Core
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.TypeInfoResolverChain.Insert(0, AppJsonContext.Default);
});
```

### Benefits

- **No reflection at runtime** - All type info generated at compile time
- **AOT compatible** - Works with Native AOT publishing
- **Faster** - No runtime type analysis
- **Trim-safe** - Linker knows exactly what's needed

---

## Protocol Buffers (Protobuf)

Best for: Actor systems, gRPC, event sourcing, any long-lived wire format.

### Setup

```bash
dotnet add package Google.Protobuf
dotnet add package Grpc.Tools
```

### Define Schema

```protobuf
// orders.proto
syntax = "proto3";

message Order {
    string id = 1;
    string customer_id = 2;
    repeated OrderItem items = 3;
    int64 created_at_ticks = 4;

    // Adding new fields is always safe
    string notes = 5;  // Added in v2 - old readers ignore it
}

message OrderItem {
    string product_id = 1;
    int32 quantity = 2;
    int64 price_cents = 3;
}
```

### Versioning Rules

```protobuf
// SAFE: Add new fields with new numbers
message Order {
    string id = 1;
    string customer_id = 2;
    string shipping_address = 5;  // NEW - safe
}

// SAFE: Remove fields (old readers ignore unknown, new readers use default)
// Just stop using the field, keep the number reserved
message Order {
    string id = 1;
    // customer_id removed, but field 2 is reserved
    reserved 2;
}

// UNSAFE: Change field types
message Order {
    int32 id = 1;  // Was: string - BREAKS!
}

// UNSAFE: Reuse field numbers
message Order {
    reserved 2;
    string new_field = 2;  // Reusing 2 - BREAKS!
}
```

---

## MessagePack

Best for: High-performance scenarios, compact payloads, actor messaging.

### Setup

```bash
dotnet add package MessagePack
dotnet add package MessagePack.Annotations
```

### Usage with Contracts

```csharp
[MessagePackObject]
public sealed class Order
{
    [Key(0)]
    public required string Id { get; init; }

    [Key(1)]
    public required string CustomerId { get; init; }

    [Key(2)]
    public required IReadOnlyList<OrderItem> Items { get; init; }

    [Key(3)]
    public required DateTimeOffset CreatedAt { get; init; }

    // New field - old readers skip unknown keys
    [Key(4)]
    public string? Notes { get; init; }
}

// Serialize
var bytes = MessagePackSerializer.Serialize(order);

// Deserialize
var order = MessagePackSerializer.Deserialize<Order>(bytes);
```

### AOT-Compatible Setup

```csharp
// Use source generator for AOT
[MessagePackObject]
public partial class Order { }  // Illustrative contract; verify generator requirements for the pinned package

// Current StandardResolver discovers generated formatters and retains built-in/collection support.
// Verify source generation and AOT support for every contract in the pinned package.
var options = MessagePackSerializerOptions.Standard;
```

---

## Migrating from Newtonsoft.Json

### Common Issues

| Newtonsoft | System.Text.Json | Fix |
|------------|------------------|-----|
| `$type` in JSON | Not supported by default | Use discriminators or custom converters |
| `JsonProperty` | `JsonPropertyName` | Different attribute |
| `DefaultValueHandling` | `DefaultIgnoreCondition` | Different API |
| `NullValueHandling` | `DefaultIgnoreCondition` | Different API |
| Private setters | Requires `[JsonInclude]` | Explicit opt-in |
| Polymorphism | `[JsonDerivedType]` (.NET 7+) | Explicit discriminators |

### Migration Pattern

```csharp
// Newtonsoft (commonly reflection-based; type metadata is configuration-dependent)
public class Order
{
    [JsonProperty("order_id")]
    public string Id { get; set; }

    [JsonProperty(NullValueHandling = NullValueHandling.Ignore)]
    public string? Notes { get; set; }
}

// System.Text.Json (source-gen compatible)
public sealed record Order(
    [property: JsonPropertyName("order_id")]
    string Id,

    string? Notes  // Null handling via JsonSerializerOptions
);

[JsonSerializable(typeof(Order))]
[JsonSourceGenerationOptions(
    PropertyNamingPolicy = JsonKnownNamingPolicy.SnakeCaseLower,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull)]
public partial class OrderJsonContext : JsonSerializerContext { }
```

### Polymorphism with Discriminators

```csharp
// .NET 7+ polymorphism
[JsonDerivedType(typeof(CreditCardPayment), "credit_card")]
[JsonDerivedType(typeof(BankTransferPayment), "bank_transfer")]
public abstract record Payment(decimal Amount);

public sealed record CreditCardPayment(decimal Amount, string Last4) : Payment(Amount);
public sealed record BankTransferPayment(decimal Amount, string AccountNumber) : Payment(Amount);

// Serializes as:
// { "$type": "credit_card", "amount": 100, "last4": "1234" }
```

---

## Wire Compatibility Patterns

### Tolerant Reader

Old code must safely ignore unknown fields:

```csharp
// Protobuf/MessagePack: unknown-field handling depends on the schema/contract shape
// System.Text.Json: configure to allow
var options = new JsonSerializerOptions
{
    UnmappedMemberHandling = JsonUnmappedMemberHandling.Skip
};
```

### Introduce Read Before Write

Deploy deserializers before serializers for new formats:

```csharp
// Phase 1: Add deserializer (deployed everywhere)
public Order Deserialize(byte[] data, string manifest) => manifest switch
{
    "Order.V1" => DeserializeV1(data),
    "Order.V2" => DeserializeV2(data),  // NEW - can read V2
    _ => throw new NotSupportedException()
};

// Phase 2: Enable serializer (next release, after V1 deployed everywhere)
public (byte[] data, string manifest) Serialize(Order order) =>
    _useV2Format
        ? (SerializeV2(order), "Order.V2")
        : (SerializeV1(order), "Order.V1");
```

### Never Embed Type Names

```csharp
// BAD: Type name in payload - renaming class breaks wire format
{
    "$type": "MyApp.Order, MyApp.Core",
    "id": "123"
}

// GOOD: Explicit discriminator - refactoring safe
{
    "type": "order",
    "id": "123"
}
```

---

## Performance Comparison

Approximate throughput (higher is better):

| Format | Serialize | Deserialize | Size |
|--------|-----------|-------------|------|
| MessagePack | ★★★★★ | ★★★★★ | ★★★★★ |
| Protobuf | ★★★★★ | ★★★★★ | ★★★★★ |
| System.Text.Json (source gen) | ★★★★☆ | ★★★★☆ | ★★★☆☆ |
| System.Text.Json (reflection) | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ |
| Newtonsoft.Json | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ |

For hot paths, prefer MessagePack or Protobuf.

---

## Akka.NET Serialization

For Akka.NET actor systems, use schema-based serialization:

```hocon
akka {
  actor {
    serializers {
      messagepack = "Akka.Serialization.MessagePackSerializer, Akka.Serialization.MessagePack"
    }
    serialization-bindings {
      "MyApp.Messages.IMessage, MyApp" = messagepack
    }
  }
}
```

See [Akka.NET Serialization Docs](https://getakka.net/articles/networking/serialization.html).

---

## Best Practices

### DO

```csharp
// Use source generators for System.Text.Json
[JsonSerializable(typeof(Order))]
public partial class AppJsonContext : JsonSerializerContext { }

// Use explicit field numbers/keys
[MessagePackObject]
public class Order
{
    [Key(0)] public string Id { get; init; }
}

// Use records for immutable message types
public sealed record OrderCreated(OrderId Id, CustomerId CustomerId);
```

### DON'T

```csharp
// Don't use BinaryFormatter (ever)
var formatter = new BinaryFormatter();  // Security risk!

// Avoid CLR type-name metadata in wire contracts unless explicitly required
settings.TypeNameHandling = TypeNameHandling.All;  // Couples payloads to CLR type identities

// Don't use reflection serialization for hot paths (institutional preference).
// Newtonsoft.Json's reflection-based defaults are not trim/Native-AOT safe; benchmark hot paths.
JsonConvert.SerializeObject(order);
```

Starting with .NET 9, the in-box BinaryFormatter implementation throws `PlatformNotSupportedException`. Do not restore it with the unsupported compatibility package; see [Microsoft's migration guidance](https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide). For Newtonsoft.Json, avoid accepting untrusted CLR type metadata; `TypeNameHandling` is not a safe default for external payloads.

---

## Resources

- **System.Text.Json Source Generation**: https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation
- **Protocol Buffers**: https://protobuf.dev/
- **MessagePack-CSharp**: https://github.com/MessagePack-CSharp/MessagePack-CSharp
- **Akka.NET Serialization**: https://getakka.net/articles/networking/serialization.html
- **Wire Compatibility**: https://getakka.net/community/contributing/wire-compatibility.html
