using System.Collections;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Dynamic;
using System.Linq;
using DormPortal.Data;
using DormPortal.Web.Helpers;
using Xunit;

namespace DormPortal.Tests.Web
{
    public class QueryableShaperShould
    {
		[Fact]
		public void GetOnlyPassportNumberWhenShapeStudent2()
		{
			var students = DummyData.Students;

			var shapedStudents = students.AsQueryable().ShapeData("PassportNumber");
			var firstElement = shapedStudents.ElementAt(0) as IDictionary<string, object>;
			Assert.Equal("484245aa", firstElement["PassportNumber"]);
		}
	}
}
