using MessagePack;
/* OPTIONS_FROM_SKILL */
var input = new Order { Id = Guid.NewGuid(), Items = new List<Guid> { Guid.NewGuid() } };
var bytes = MessagePackSerializer.Serialize(input, options);
var output = MessagePackSerializer.Deserialize<Order>(bytes, options);
if (input.Id != output.Id || input.Items[0] != output.Items[0]) throw new Exception("Round trip failed");
Console.WriteLine("Nested Guid/list round trip passed");
[MessagePackObject]
public partial class Order {
    [Key(0)] public Guid Id {get; set;}
    [Key(1)] public List<Guid> Items {get; set;}
}
