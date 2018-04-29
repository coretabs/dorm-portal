using System.Linq;
using DormPortal.Data;
using DormPortal.Web.Helpers;
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

			Assert.Equal(shapedStudents[0], "");

			Assert.Equal(typeof(EnumerableQuery<string>), shapedStudents.GetType());
		}
    }
}
