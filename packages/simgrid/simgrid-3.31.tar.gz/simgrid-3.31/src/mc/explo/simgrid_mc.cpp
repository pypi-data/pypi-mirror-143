/* Copyright (c) 2015-2022. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/sg_config.hpp"
#include "src/internal_config.h"
#include "src/mc/explo/Exploration.hpp"
#include "src/mc/mc_config.hpp"
#include "src/mc/mc_exit.hpp"

#if HAVE_SMPI
#include "smpi/smpi.h"
#endif

#include <cstring>
#include <memory>
#include <unistd.h>

int main(int argc, char** argv)
{
  xbt_assert(argc >= 2, "Missing arguments");

  // Currently, we need this before sg_config_init:
  _sg_do_model_check = 1;

  // The initialization function can touch argv.
  // We make a copy of argv before modifying it in order to pass the original value to the model-checked application:
  std::vector<char*> argv_copy{argv, argv + argc + 1};

  xbt_log_init(&argc, argv);
#if HAVE_SMPI
  smpi_init_options(); // only performed once
#endif
  sg_config_init(&argc, argv);

  simgrid::mc::ExplorationAlgorithm algo;
  if (_sg_mc_comms_determinism || _sg_mc_send_determinism)
    algo = simgrid::mc::ExplorationAlgorithm::CommDeterminism;
  else if (_sg_mc_unfolding_checker)
    algo = simgrid::mc::ExplorationAlgorithm::UDPOR;
  else if (_sg_mc_property_file.get().empty())
    algo = simgrid::mc::ExplorationAlgorithm::Safety;
  else
    algo = simgrid::mc::ExplorationAlgorithm::Liveness;

  int res      = SIMGRID_MC_EXIT_SUCCESS;
  std::unique_ptr<simgrid::mc::Exploration> checker{simgrid::mc::Api::get().initialize(argv_copy.data(), algo)};
  try {
    checker->run();
  } catch (const simgrid::mc::DeadlockError&) {
    res = SIMGRID_MC_EXIT_DEADLOCK;
  } catch (const simgrid::mc::TerminationError&) {
    res = SIMGRID_MC_EXIT_NON_TERMINATION;
  } catch (const simgrid::mc::LivenessError&) {
    res = SIMGRID_MC_EXIT_LIVENESS;
  }
  simgrid::mc::Api::get().s_close();
  checker.release(); // FIXME: this line should not exist, but it segfaults in liveness
  return res;
}
