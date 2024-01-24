getAuth()
  .importUsers(
    [
      {
        uid: 'some-uid',
        email: 'user@example.com',
        // Must be provided in a byte buffer.
        passwordHash: Buffer.from('password-hash'),
        // Must be provided in a byte buffer.
        passwordSalt: Buffer.from('salt'),
      },
    ],
    {
      hash: {
        algorithm: 'PBKDF2_SHA256',
        rounds: 100000,
      },
    }
  )
  .then((results) => {
    results.errors.forEach((indexedError) => {
      console.log(`Error importing user ${indexedError.index}`);
    });
  })
  .catch((error) => {
    console.log('Error importing users :', error);
  });