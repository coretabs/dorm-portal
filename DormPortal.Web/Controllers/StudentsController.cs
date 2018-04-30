using System;
using System.Collections.Generic;
using AutoMapper;
using DormPortal.Core.Dtos;
using DormPortal.Core.Helpers;
using DormPortal.Core.Models;
using DormPortal.Data;
using DormPortal.Web.Helpers;
using Microsoft.AspNetCore.JsonPatch;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Sieve.Services;

namespace DormPortal.Web.Controllers
{
	[Route("api/[controller]")]
	public class StudentsController : Controller
	{
		private readonly IUnitOfWork _unitOfWork;
		private readonly ILogger<StudentsController> _logger;
		private readonly ISieveProcessor _sieveProcessor;

		public StudentsController(IUnitOfWork unitOfWork, ILogger<StudentsController> logger, 
			ISieveProcessor sieveProcessor)
		{
			_unitOfWork = unitOfWork;
			_logger = logger;
			_sieveProcessor = sieveProcessor;
		}

		[HttpGet]
		public IActionResult Get(SieveModel sieveModel)
		{
			IActionResult result;
			var students = _unitOfWork.StudentRepository.GetAll();

			try
			{
				result = Ok(QueryableSieve.Apply(_sieveProcessor, sieveModel, students));
			}
			catch (Exception)
			{
				result = BadRequest();
			}

			return result;
		}

		[HttpGet("{id}", Name = "GET")]
		public IActionResult Get(int id)
		{
			IActionResult result;

			try
			{
				var student = _unitOfWork.StudentRepository.FindById(id);
				result = Ok(Mapper.Map<StudentDto>(student));
			}
			catch (KeyNotFoundException)
			{
				result = NotFound("Could not find the entity with this id");
			}

			return result;
		}

		[HttpPost]
		public IActionResult Post([FromBody] StudentForCreationDto studentDto)
		{
			IActionResult result;

			if (ModelState.IsValid(out result, new []{ studentDto }))
			{
				var student = _unitOfWork.StudentRepository.Add(Mapper.Map<Student>(studentDto));

				if (_unitOfWork.Commit())
				{
					result = CreatedAtRoute("GET", new { id = student.Id }, Mapper.Map<StudentDto>(student));
				}
				else
				{
					throw new Exception("Creating entity failed");
				}

				_logger.LogInformation($"Added a new student entity {student.Id}");
			}

			

			return result;
		}

		[HttpPut("{id}")]
		public IActionResult Put(int id, [FromBody] StudentForUpdateDto studentDto)
		{
			IActionResult result;

			if (ModelState.IsValid(out result, new[] { studentDto }))
			{
				try
				{
					var student = _unitOfWork.StudentRepository.FindById(id);
					Mapper.Map(studentDto, student);

					_unitOfWork.StudentRepository.Update(student);
					_unitOfWork.Commit();
					result = Ok(student);
					_logger.LogInformation($"Updated a student entity {student.Id}");
				}
				catch (KeyNotFoundException)
				{
					result = NotFound("Could not find the entity with this id");
				}
			}

			return result;
		}

		[HttpPatch("{id}")]
		public IActionResult Patch(int id, [FromBody] JsonPatchDocument<StudentForUpdateDto> studentPatch)
		{
			IActionResult result;

			if (ModelState.IsValid(out result, new[] { studentPatch }))
			{
				try
				{
					var student = _unitOfWork.StudentRepository.FindById(id);
					var studentDto = Mapper.Map<StudentForUpdateDto>(student);
					studentPatch.ApplyTo(studentDto, ModelState);
					TryValidateModel(studentDto);

					if (ModelState.IsValid(out result))
					{
						Mapper.Map(studentDto, student);

						_unitOfWork.StudentRepository.Update(student);
						_unitOfWork.Commit();
						result = Ok(student);
					}

					_logger.LogInformation($"Updated a student entity {student.Id}");
				}
				catch (KeyNotFoundException)
				{
					result = NotFound("Could not find the entity with this id");
				}
			}

			return result;
		}

		[HttpDelete("{id}")]
		public IActionResult Delete(int id)
		{
			IActionResult result;

			try
			{
				_unitOfWork.StudentRepository.Delete(id);
				_unitOfWork.Commit();
				result = NoContent();
				_logger.LogInformation($"Deleted a student entity {id}");
			}
			catch (DbUpdateConcurrencyException)
			{
				result = NotFound("Could not find the entity with this id");
			}

			return result;
		}
	}
}
