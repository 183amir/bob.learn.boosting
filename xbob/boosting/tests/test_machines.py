import xbob.boosting
import numpy
import bob
import nose
import os
import tempfile
import xbob.io


def test_machine():
  # test the stump machine
  stump = xbob.boosting.machine.StumpMachine(0., 1., 0)

  scores = numpy.ndarray((1,), numpy.float64)
  stump(numpy.ones((1,1), dtype=numpy.uint16), scores)
  nose.tools.eq_(scores[0], 1)

  score = stump(numpy.ones((1,), dtype=numpy.float64))
  nose.tools.eq_(scores, 1)

  nose.tools.eq_(stump.threshold, 0.)
  nose.tools.eq_(stump.polarity, 1.)

  temp = tempfile.mkstemp(prefix = "xbbst_", suffix=".hdf5")[1]
  f = xbob.io.HDF5File(temp, 'w')
  stump.save(f)

  stump2 = xbob.boosting.machine.StumpMachine(f)
  nose.tools.eq_(stump2.threshold, 0.)
  nose.tools.eq_(stump2.polarity, 1.)
  del f
  os.remove(temp)

  # test the LUT machine
  LUT = numpy.ones((1,1), numpy.float)
  indices = numpy.zeros((1,), numpy.int32)
  machine = xbob.boosting.machine.LUTMachine(LUT, indices)

  score = machine(numpy.zeros((1,), dtype=numpy.uint16))
  nose.tools.eq_(score, 1)

  assert(numpy.allclose(machine.lut, LUT))

  temp = tempfile.mkstemp(prefix = "xbbst_", suffix=".hdf5")[1]
  f = xbob.io.HDF5File(temp, 'w')
  machine.save(f)

  machine2 = xbob.boosting.machine.LUTMachine(f)
  assert(numpy.allclose(machine2.lut, LUT))
  del f
  os.remove(temp)

  boosted_machine = xbob.boosting.machine.BoostedMachine()
  boosted_machine.add_weak_machine(stump, 1.)
  boosted_machine.add_weak_machine(machine, 1.)

  score = boosted_machine(numpy.zeros((1,), dtype=numpy.uint16))
  nose.tools.eq_(score, 2)

  scores = numpy.ndarray((1,), numpy.float64)
  labels = numpy.ndarray((1,), numpy.float64)
  boosted_machine(numpy.zeros((1,1), dtype=numpy.uint16), scores, labels)
  nose.tools.eq_(scores[0], 2)
  nose.tools.eq_(labels[0], 1)

  # check IO functionality
  file = tempfile.mkstemp(prefix='xbob_test_')[1]
  boosted_machine.save(xbob.io.HDF5File(file, 'w'))
  new_machine = xbob.boosting.machine.BoostedMachine(xbob.io.HDF5File(file))
  os.remove(file)
  assert (new_machine.alpha == 1).all()

  # forward some features with the new strong machine
  score = new_machine(numpy.zeros((1,), dtype=numpy.uint16))
  nose.tools.eq_(score, 2)

  scores = numpy.ndarray((1,), numpy.float64)
  new_machine(numpy.zeros((1,1), dtype=numpy.uint16), scores)
  nose.tools.eq_(scores[0], 2)

  labels = numpy.ndarray((1,), numpy.float64)
  new_machine(numpy.zeros((1,1), dtype=numpy.uint16), scores, labels)
  nose.tools.eq_(scores[0], 2)
  nose.tools.eq_(labels[0], 1)

if __name__ == '__main__':
  test_machine()
