# ERP data is synced read-only into our own store

Line schedule, sample room loading and material lead times are read from the in-house ERP with a read-only account and copied on a schedule into the structured store; agents query only that copy. This avoids loading the ERP and removes any chance of corrupting it. Until IT grants access, the same loader reads Excel exports from the ERP.
