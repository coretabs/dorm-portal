using System.Linq;
using DormPortal.Data;
using DormPortal.Web.Extensions;
using Xunit;

namespace DormPortal.Tests.Web
{
    public class QueryableShaperShould
    {
        [Fact]
        public void GetOnlyPassportNumberWhenShapeStudent()
        {
	        var students = DummyData.Students;

	        var shapedStudents = students.AsQueryable().Shape(new []{ "passportNumber" });

			Assert.Equal(typeof(EnumerableQuery<string>), shapedStudents.GetType());
		}
    }
}
