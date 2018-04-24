using System;
using System.Linq;
using DormPortal.Core.Models;
using DormPortal.Data;
using Microsoft.AspNetCore.Mvc;

namespace DormPortal.Web.Controllers
{
	[Route("api/[controller]")]
	public class StudentsController : Controller
    {
	    private readonly IUnitOfWork _unitOfWork;

	    public StudentsController(IUnitOfWork unitOfWork)
	    {
		    _unitOfWork = unitOfWork;
	    }

		[HttpGet]
	    public IActionResult Get()
		{
			return Ok(_unitOfWork.StudentRepository.GetAll().Select(x => new
			{
				name = x.Name,
				passportNumber = x.PassportNumber,
			}).ToList());
	    }

	    public IActionResult Get(int id)
	    {
		    return Ok(_unitOfWork.StudentRepository.FindById(id));
	    }

	    public IActionResult Post(Student student)
	    {
		    //var result = _unitOfWork.Add<Student>(student);
		    var result = student;
		    _unitOfWork.Commit();

		    return Ok(result);
	    }

	    public IActionResult Put(int id, Student student)
	    {
		    var studentToUpdate = _unitOfWork.StudentRepository.FindById(id);
		    //var result = _unitOfWork.Update(student);
		    _unitOfWork.Commit();

		    //return Ok(result);
		    return Ok("");
		}

	  //  public IActionResult Delete(Student student)
	  //  {
			//var result = _unitOfWork.Delete(student);
		 //   _unitOfWork.Commit();

		 //   return Ok(result);
	  //  }
	}
}
